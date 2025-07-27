import streamlit as st
from rag_chain import GrokRagChain
from strategy_table import get_action, get_action_text

# Page configuration
st.set_page_config(
    page_title="Grok21 - Blackjack Strategy Helper",
    page_icon="🃏",
    layout="centered"
)

# Modern, clean color scheme inspired by 2025 UI trends
st.markdown("""
<style>
/* Modern neutral background with proper contrast */
.stApp {
    background-color: #fafafa;
    color: #2d3748;
}

.main .block-container {
    padding-top: 2rem;
    max-width: 800px;
    background-color: #ffffff;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    padding: 2rem;
    margin-top: 1rem;
}

/* Clean input styling with subtle borders */
.stSelectbox > div > div, .stNumberInput > div > div > input {
    background-color: #ffffff;
    border: 2px solid #e2e8f0;
    border-radius: 8px;
    color: #2d3748;
}

.stSelectbox > div > div:focus-within, .stNumberInput > div > div:focus-within {
    border-color: #4299e1;
    box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.1);
}

/* Modern button with gradient */
.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.75rem 1.5rem;
    font-weight: 600;
    width: 100%;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 15px rgba(102, 126, 234, 0.3);
}

/* Strategy result with modern card design */
.action-result {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 12px;
    padding: 2rem;
    margin: 2rem 0;
    text-align: center;
    font-size: 1.5rem;
    font-weight: 700;
    box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
}

/* RAG response with clean styling */
.rag-response {
    background-color: #f7fafc;
    border-left: 4px solid #48bb78;
    padding: 1.5rem;
    margin: 1.5rem 0;
    border-radius: 8px;
    color: #2d3748;
    line-height: 1.6;
}

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 2rem;
}

.stTabs [data-baseweb="tab"] {
    color: #718096;
    font-weight: 600;
}

.stTabs [aria-selected="true"] {
    color: #667eea;
}

/* Text area styling */
.stTextArea textarea {
    background-color: #ffffff;
    border: 2px solid #e2e8f0;
    border-radius: 8px;
    color: #2d3748;
}

.stTextArea textarea:focus {
    border-color: #4299e1;
    box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.1);
}

/* Headers with better contrast */
h1, h2, h3 {
    color: #2d3748 !important;
}

.stMarkdown {
    color: #4a5568;
}
</style>
""", unsafe_allow_html=True)

# Initialize RAG chain
@st.cache_resource
def init_rag_chain():
    return GrokRagChain()

try:
    rag_chain = init_rag_chain()
except Exception as e:
    st.error(f"Error initializing RAG chain: {e}")
    st.stop()

# Title
st.title("🃏 Grok21 - Blackjack Strategy")
st.markdown("**Simple. Fast. Optimal.**")

# Main tabs
tab1, tab2 = st.tabs(["🎯 Quick Strategy", "💬 Ask Questions"])

with tab1:
    st.subheader("Get Your Play")
    
    # Simple input form
    col1, col2, col3 = st.columns(3)
    
    with col1:
        player_total = st.number_input(
            "Your Hand Total", 
            min_value=5, 
            max_value=21, 
            value=12
        )
    
    with col2:
        dealer_upcard = st.selectbox(
            "Dealer Shows",
            options=[2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
            index=8,
            format_func=lambda x: "A" if x == 11 else str(x)
        )
    
    with col3:
        hand_type = st.selectbox(
            "Hand Type",
            options=["hard", "soft", "pair"],
            format_func=lambda x: x.title()
        )
    
    # Get strategy button
    if st.button("Get Strategy", type="primary"):
        try:
            action_code = get_action(hand_type, player_total, dealer_upcard)
            action_text = get_action_text(action_code)
            
            st.markdown(f"""
            <div class="action-result">
                {action_text}
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error: {e}")

with tab2:
    st.subheader("Learn Strategy")
    
    # Question input
    question = st.text_area(
        "Ask about blackjack strategy:",
        placeholder="Why should I hit 16 vs dealer 10?",
        height=100
    )
    
    if st.button("Ask Grok", type="primary"):
        if question.strip():
            with st.spinner("Thinking..."):
                try:
                    response = rag_chain.get_response(question)
                    
                    st.markdown(f"""
                    <div class="rag-response">
                        {response}
                    </div>
                    """, unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"Error getting response: {e}")
        else:
            st.warning("Please enter a question!")
    
    # Example questions
    with st.expander("💡 Example Questions"):
        st.markdown("""
        - Why hit 16 vs dealer 10?
        - When should I double down?
        - What's the difference between hard and soft hands?
        - Why never split 10s?
        - How does basic strategy work?
        """)

# Footer
st.markdown("---")
st.markdown("*Use basic strategy for optimal blackjack play*")