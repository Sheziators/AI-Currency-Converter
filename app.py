import streamlit as st
import requests
import json
import os
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

# ------------------------------------------------------------------
# 1. Page config
# ------------------------------------------------------------------
st.set_page_config(page_title="💱 LLM Currency Converter", page_icon="💵", layout="wide")

# ------------------------------------------------------------------
# 2. Custom CSS
# ------------------------------------------------------------------
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .info-text {
        text-align: center;
        color: #666;
        margin-bottom: 1rem;
    }
    .conversion-details {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .metric-label {
        font-weight: bold;
        font-size: 1rem;
    }
    .metric-value {
        font-size: 1.2rem;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# 3. Currency symbols mapping
# ------------------------------------------------------------------
CURRENCY_SYMBOLS = {
    "USD": "$", "EUR": "€", "GBP": "£", "JPY": "¥", "INR": "₹",
    "CAD": "C$", "AUD": "A$", "CHF": "Fr", "CNY": "¥", "SEK": "kr",
    "NZD": "NZ$", "MXN": "$", "SGD": "S$", "HKD": "HK$", "NOK": "kr",
    "KRW": "₩", "TRY": "₺", "RUB": "₽", "BRL": "R$", "ZAR": "R"
}

# ------------------------------------------------------------------
# 4. Header
# ------------------------------------------------------------------
st.markdown('<div class="main-header">💱 AI Currency Converter</div>', unsafe_allow_html=True)
st.markdown("""
    <div class="info-text">
        Ask me to convert any amount – for example: <i>"Convert 100 USD to EUR"</i>
    </div>
""", unsafe_allow_html=True)
st.markdown("---")

# ------------------------------------------------------------------
# 5. Define tools
# ------------------------------------------------------------------
@tool(description="Fetch the real‑time conversion rate between two currencies.")
def get_conversion_factor(base_currency: str, target_currency: str) -> dict:
    url = f"https://v6.exchangerate-api.com/v6/754715f6d48aac37d37e5f25/pair/{base_currency}/{target_currency}"
    response = requests.get(url, timeout=10)
    return response.json()

@tool(description="Calculate the target currency amount given a value and a conversion rate.")
def convert(base_currency_value: float, conversion_rate: float) -> float:
    return base_currency_value * conversion_rate

# ------------------------------------------------------------------
# 6. Get Hugging Face token from environment variable (for GitHub)
# ------------------------------------------------------------------
HF_TOKEN = os.environ.get("HUGGINGFACEHUB_ACCESS_TOKEN")
if not HF_TOKEN:
    st.error("""
    ❌ Hugging Face token not found.  
    Please set the environment variable `HUGGINGFACEHUB_ACCESS_TOKEN`  
    or add it to Streamlit secrets.
    """)
    st.stop()

# ------------------------------------------------------------------
# 7. Load LLM with tools (cached)
# ------------------------------------------------------------------
@st.cache_resource
def load_llm_with_tools():
    llm_instance = HuggingFaceEndpoint(
        repo_id="Qwen/Qwen2.5-7B-Instruct",
        task="text-generation",
        max_new_tokens=512,
        temperature=0.1,
        huggingfacehub_api_token=HF_TOKEN,
    )
    llm = ChatHuggingFace(llm=llm_instance)
    return llm.bind_tools([get_conversion_factor, convert])

llm_with_tools = load_llm_with_tools()

# ------------------------------------------------------------------
# 8. Execute tool calls
# ------------------------------------------------------------------
def execute_tool_calls(ai_message: AIMessage) -> tuple[list[ToolMessage], dict]:
    tool_messages = []
    conversion_data = {
        "amount": None,
        "base": None,
        "target": None,
        "rate": None,
        "result": None,
        "time": None
    }

    rate_calls = []
    convert_calls = []
    for tc in ai_message.tool_calls:
        if tc["name"] == "get_conversion_factor":
            rate_calls.append(tc)
        elif tc["name"] == "convert":
            convert_calls.append(tc)

    for tc in rate_calls:
        result = get_conversion_factor.invoke(tc["args"])
        if result.get("result") == "success" and "conversion_rate" in result:
            conversion_data["rate"] = result["conversion_rate"]
            conversion_data["base"] = result.get("base_code")
            conversion_data["target"] = result.get("target_code")
            conversion_data["time"] = result.get("time_last_update_utc", "real‑time")
            tool_messages.append(
                ToolMessage(content=json.dumps(result), name=tc["name"], tool_call_id=tc["id"])
            )
        else:
            error_msg = f"Failed to get conversion rate: {result.get('error-type', 'unknown error')}"
            tool_messages.append(
                ToolMessage(content=error_msg, name=tc["name"], tool_call_id=tc["id"])
            )

    for tc in convert_calls:
        if conversion_data["rate"] is None:
            error_msg = "Cannot convert: no valid conversion rate available. Please try again."
            tool_messages.append(
                ToolMessage(content=error_msg, name=tc["name"], tool_call_id=tc["id"])
            )
        else:
            amount = tc["args"].get("base_currency_value")
            conversion_data["amount"] = amount
            args = tc["args"].copy()
            args["conversion_rate"] = conversion_data["rate"]
            result = convert.invoke(args)
            conversion_data["result"] = result
            tool_messages.append(
                ToolMessage(content=str(result), name=tc["name"], tool_call_id=tc["id"])
            )

    return tool_messages, conversion_data

# ------------------------------------------------------------------
# 9. Display formatted conversion box
# ------------------------------------------------------------------
def display_conversion_box(data: dict):
    if data["result"] is None or data["amount"] is None:
        return
    amount = data["amount"]
    base = data["base"]
    target = data["target"]
    rate = data["rate"]
    result = data["result"]
    base_symbol = CURRENCY_SYMBOLS.get(base, base)
    target_symbol = CURRENCY_SYMBOLS.get(target, target)

    st.markdown("✅ **Conversion complete**")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="metric-label">Amount</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{base_symbol}{amount:,.2f} ({base})</div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-label">Exchange Rate</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">1 {base} = {rate:.4f} {target}</div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-label">Converted</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{target_symbol}{result:,.2f} ({target})</div>', unsafe_allow_html=True)
    st.caption(f"📅 Last updated: {data['time']}")
    st.caption("Exchange rates are live. For exact rates, always check a reliable source.")

# ------------------------------------------------------------------
# 10. Chat UI with persistent history
# ------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.markdown(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            if hasattr(msg, "conversion_data") and msg.conversion_data["result"]:
                display_conversion_box(msg.conversion_data)
            else:
                st.markdown(msg.content)

if prompt := st.chat_input("Ask me to convert currencies..."):
    user_msg = HumanMessage(content=prompt)
    st.session_state.messages.append(user_msg)
    with st.chat_message("user"):
        st.markdown(prompt)

    ai_msg = llm_with_tools.invoke(st.session_state.messages)
    st.session_state.messages.append(ai_msg)

    if ai_msg.tool_calls:
        tool_msgs, conv_data = execute_tool_calls(ai_msg)
        st.session_state.messages.extend(tool_msgs)

        final_answer = llm_with_tools.invoke(st.session_state.messages)
        if conv_data["result"]:
            special_msg = AIMessage(content="✅ Conversion complete")
            special_msg.conversion_data = conv_data
            st.session_state.messages.append(special_msg)
            with st.chat_message("assistant"):
                display_conversion_box(conv_data)
        else:
            st.session_state.messages.append(final_answer)
            with st.chat_message("assistant"):
                st.markdown(final_answer.content)
    else:
        st.session_state.messages.append(ai_msg)
        with st.chat_message("assistant"):
            st.markdown(ai_msg.content)

# ------------------------------------------------------------------
# 11. Sidebar
# ------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ℹ️ About")
    st.info("""
    **AI Currency Converter Features:**
    - Powered by Hugging Face LLM (Qwen 2.5)
    - Real‑time exchange rates via ExchangeRate-API
    - Natural language understanding
    - Tool‑calling for accurate conversions
    """)

    st.markdown("### 📋 Supported Currencies")
    currencies = {
        "USD": "US Dollar", "EUR": "Euro", "GBP": "British Pound",
        "JPY": "Japanese Yen", "INR": "Indian Rupee", "CAD": "Canadian Dollar",
        "AUD": "Australian Dollar", "CHF": "Swiss Franc", "CNY": "Chinese Yuan"
    }
    for code, name in currencies.items():
        symbol = CURRENCY_SYMBOLS.get(code, "")
        st.write(f"**{code}** {symbol} – {name}")
    st.write("... and many more via API")

    st.markdown("### 💡 Try these examples")
    st.markdown("""
    - `Convert 100 USD to EUR`
    - `What is 50 GBP in INR?`
    - `How much is 1000 Japanese Yen in US Dollars?`
    """)