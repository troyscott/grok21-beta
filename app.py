import streamlit as st
import os  # For os.getenv
from rag_chain import GrokRagChain

st.title("Grok21: Blackjack Assistant 🎴")
if "rag" not in st.session_state:
    try:
        st.session_state.rag = GrokRagChain(model=os.getenv("GROK_MODEL"))
    except ValueError as e:
        st.error(str(e))
        st.stop()
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome! Get instant advice in the sidebar or ask me strategy questions here. 🚀"}
    ]

# Sidebar for quick hand advice - Clean, crisp, and engaging
with st.sidebar:
    st.header("Your Next Move")
    hand_type = st.selectbox("Hand", ["hard", "soft", "pair"], key="hand_type_select")
    player_value = st.number_input("Your Total", min_value=2, max_value=21, value=10, key="player_value_input")
    dealer_upcard = st.number_input("Dealer Card", min_value=2, max_value=11, value=10, key="dealer_upcard_input")
    if st.button("Get Move"):
        advice = st.session_state.rag.get_response("", hand_type, player_value, dealer_upcard)
        action, explanation = advice.split(". ", 1)
        action_code = action.split(": ")[1]
        icon_map = {'H': '🔴', 'S': '🟢', 'D': '🔵', 'Ds': '🔵', 'P': '🟣'}
        tip_map = {
            'H': '💡 Hit boosts your odds ~20%!',
            'S': '💡 Stand wins ~30% vs. weak dealers!',
            'D': '💡 Double for up to 2x gains!'
        }
        st.markdown(f"**{icon_map.get(action_code, '⚫')} {action}**")
        st.write(f"Why: {explanation}")
        st.write(tip_map.get(action_code, '💡 Stick to strategy to beat the house!'))
        if st.button("Why This Move?"):
            auto_prompt = f"Why {action_code} on {hand_type} {player_value} vs. {dealer_upcard}?"
            st.session_state.messages.append({"role": "user", "content": auto_prompt})
            with st.chat_message("user"):
                st.markdown(auto_prompt)
            with st.spinner("Thinking..."):
                response = st.session_state.rag.get_response(auto_prompt)
            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# Chat for detailed insights - Minimal and guided
st.header("Strategy Chat")
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        st.write(" ")  # Add spacing for readability

if prompt := st.chat_input("Ask a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.spinner("Thinking..."):
        response = st.session_state.rag.get_response(prompt)
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})