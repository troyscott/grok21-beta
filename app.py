import streamlit as st
from blackjack_game import get_strategy_advice, ask_grok_question

# Page configuration
st.set_page_config(
    page_title="Grok21 - Blackjack Strategy Helper",
    page_icon="🃏",
    layout="wide"
)

# Custom CSS for clean, compact design
st.markdown("""
<style>
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 1200px;
    }
    
    .main-title {
        color: #1f1f1f;
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .stButton button {
        width: 100%;
        height: 40px;
        font-size: 15px;
        font-weight: 600;
        border-radius: 6px;
        margin: 4px 0;
    }
    
    .strategy-result {
        padding: 1rem;
        border-radius: 8px;
        background-color: #f8f9fa;
        border-left: 4px solid #007bff;
        margin: 1rem 0;
    }
    
    /* Compact input styling */
    .stNumberInput > div > div > input {
        height: 35px;
        font-size: 14px;
    }
    
    .stSelectbox > div > div > div {
        height: 35px;
        font-size: 14px;
    }
    
    .stTextArea textarea {
        height: 80px !important;
        font-size: 14px;
    }
    
    /* Reduce label spacing */
    .stNumberInput label, .stSelectbox label {
        font-size: 14px;
        margin-bottom: 2px;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-title">🃏 Grok 21 - Strategy Helper</h1>', unsafe_allow_html=True)
st.markdown("**Your companion for online blackjack games**")

# Main tabs
tab1, tab2 = st.tabs(["📊 Strategy Lookup", "🧠 Ask Grok"])

with tab1:
    st.subheader("Get Optimal Strategy Advice")
    
    # Compact input row
    col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
    
    with col1:
        player_total = st.number_input(
            "Hand Total", 
            min_value=5, 
            max_value=21, 
            value=12,
            help="Your current hand total (5-21)"
        )
    
    with col2:
        dealer_upcard = st.selectbox(
            "Dealer Upcard",
            options=[2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
            index=8,  # Default to 10
            format_func=lambda x: "Ace" if x == 11 else str(x),
            help="Dealer's visible card"
        )
    
    with col3:
        hand_type = st.selectbox(
            "Hand Type",
            options=["hard", "soft", "pair"],
            help="Hard/Soft/Pair"
        )
    
    with col4:
        st.write("")  # Empty space for alignment
        get_advice = st.button("Get Strategy", type="primary")
    
    if get_advice:
        with st.spinner("Getting optimal strategy..."):
            advice = get_strategy_advice(player_total, dealer_upcard, hand_type)
            
            st.markdown(f"""
            <div class="strategy-result">
                <strong>Recommendation:</strong><br>
                {advice}
            </div>
            """, unsafe_allow_html=True)

with tab2:
    st.subheader("Learn Blackjack Strategy with Grok")
    
    # Compact question input
    col1, col2 = st.columns([4, 1])
    
    with col1:
        question = st.text_area(
            "Ask Grok about blackjack strategy:",
            placeholder="e.g., Why do I double A-6 vs dealer 5?",
            height=60,
            label_visibility="collapsed"
        )
    
    with col2:
        st.write("")  # Space for alignment
        ask_button = st.button("Ask Grok", type="primary")
    
    # Compact example questions
    with st.expander("💡 Example Questions", expanded=False):
        st.markdown("""
        • Why hit 16 vs dealer 10? • When to double soft hands? • Hard vs soft 17 difference?  
        • How basic strategy reduces house edge? • Should I split 9s vs dealer 7?
        """)
    
    if ask_button:
        if question.strip():
            with st.spinner("Grok is thinking..."):
                response = ask_grok_question(question)
                
                st.markdown("### 🤖 Grok's Response:")
                st.markdown(response)
        else:
            st.warning("Please enter a question first!")

# Compact footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.85rem; margin-top: 1rem;'>
    🎯 Use alongside online blackjack for optimal decisions | 📚 Powered by basic strategy + Grok AI + RAG
</div>
""", unsafe_allow_html=True)