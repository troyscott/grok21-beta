import streamlit as st
from rag_chain import GrokRagChain

# Page configuration
st.set_page_config(
    page_title="Grok21",
    page_icon="🃏",
    layout="centered"
)

# Simple strategy lookup (inline for now)
def get_action(hand_type, player_total, dealer_upcard):
    """Simple basic strategy lookup"""
    if hand_type == "pair":
        if player_total == 16:  # 8s
            return "P"
        elif player_total == 2:  # Aces
            return "P"
        elif player_total >= 12:  # 6s and up
            return "S"
        else:
            return "H"
    elif hand_type == "soft":
        if player_total >= 19:
            return "S"
        elif player_total <= 17:
            return "H"
        else:
            return "S"
    else:  # hard
        if player_total >= 17:
            return "S"
        elif player_total <= 11:
            return "H"
        elif dealer_upcard <= 6:
            return "S"
        else:
            return "H"

def get_action_display(action_code):
    """Convert action code to display with icon and color"""
    actions = {
        'H': {'text': 'HIT', 'icon': '👊', 'color': '#ff4444', 'bg': '#ffe6e6'},
        'S': {'text': 'STAND', 'icon': '✋', 'color': '#4CAF50', 'bg': '#e8f5e0'},
        'D': {'text': 'DOUBLE DOWN', 'icon': '⬆️', 'color': '#2196F3', 'bg': '#e3f2fd'},
        'P': {'text': 'SPLIT', 'icon': '✂️', 'color': '#FF9800', 'bg': '#fff3e0'}
    }
    return actions.get(action_code, actions['H'])

def display_card(value, suit="♠"):
    """Display a single card using emoji/text"""
    if value == 11:
        display_value = "A"
    else:
        display_value = str(value)
    
    # Use suit emojis for better display
    suit_emoji = {"♠": "♠️", "♥": "♥️", "♦": "♦️", "♣": "♣️"}.get(suit, suit)
    
    return f"{display_value}{suit_emoji}"

def get_hand_cards(total, hand_type):
    """Get cards for display based on hand type"""
    if hand_type == "pair":
        value = total // 2
        return [display_card(value, "♠"), display_card(value, "♣")]
    elif hand_type == "soft":
        other_value = total - 11
        return [display_card(11, "♥"), display_card(other_value, "♠")]
    else:  # hard
        if total <= 11:
            first, second = total - 2, 2
        else:
            first, second = 10, total - 10
        return [display_card(first, "♠"), display_card(second, "♣")]

# Clean styling
st.markdown("""
<style>
.stApp {
    background: #fafafa;
    color: #2d3748;
}

.main .block-container {
    padding: 1rem;
    max-width: 600px;
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    margin: 0.5rem auto;
}

.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 12px;
    font-weight: 600;
    width: 100%;
    font-size: 16px;
    margin: 8px 0;
}

.card-display {
    background: linear-gradient(135deg, #e8f5e8 0%, #f0f8ff 100%);
    border-radius: 8px;
    padding: 1rem;
    margin: 1rem 0;
    text-align: center;
}

.big-cards {
    font-size: 2rem;
    margin: 0.5rem;
}

.action-result {
    border-radius: 12px;
    padding: 2rem;
    text-align: center;
    font-size: 1.5rem;
    font-weight: 700;
    margin: 1rem 0;
    border: 2px solid;
}

h1, h2, h3 {
    color: #2d3748 !important;
}
</style>
""", unsafe_allow_html=True)

# Initialize RAG
@st.cache_resource
def init_rag():
    return GrokRagChain()

try:
    rag_chain = init_rag()
except Exception as e:
    st.error(f"Error: {e}")
    st.stop()

# Header
st.title("🃏 Grok21")
st.markdown("**Simple • Fast • Optimal**")

# Tabs
tab1, tab2 = st.tabs(["🎯 Strategy", "💬 Learn"])

with tab1:
    # Inputs
    col1, col2, col3 = st.columns(3)
    
    with col1:
        player_total = st.number_input("Hand", 5, 21, 12)
    
    with col2:
        dealer_upcard = st.selectbox(
            "Dealer", 
            [2,3,4,5,6,7,8,9,10,11], 
            8,
            format_func=lambda x: "A" if x == 11 else str(x)
        )
    
    with col3:
        hand_type = st.selectbox("Type", ["hard", "soft", "pair"])
    
    # Card display using Streamlit containers
    with st.container():
        st.markdown('<div class="card-display">', unsafe_allow_html=True)
        
        # Display cards using columns
        card_col1, vs_col, card_col2 = st.columns([2, 1, 2])
        
        with card_col1:
            st.markdown(f"**Your Hand ({player_total})**")
            player_cards = get_hand_cards(player_total, hand_type)
            st.markdown(f'<div class="big-cards">{"  ".join(player_cards)}</div>', unsafe_allow_html=True)
        
        with vs_col:
            st.markdown("**VS**")
        
        with card_col2:
            st.markdown("**Dealer Shows**")
            dealer_card = display_card(dealer_upcard, "♥")
            st.markdown(f'<div class="big-cards">{dealer_card}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Strategy button
    if st.button("Get Strategy", type="primary"):
        try:
            action_code = get_action(hand_type, player_total, dealer_upcard)
            action_info = get_action_display(action_code)
            
            # Display result with custom styling and icon
            st.markdown(f"""
            <div class="action-result" style="
                color: {action_info['color']}; 
                background-color: {action_info['bg']};
                border-color: {action_info['color']};
            ">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">
                    {action_info['icon']}
                </div>
                <div>
                    {action_info['text']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error: {e}")

with tab2:
    # Question input
    question = st.text_area(
        "Ask about strategy:",
        placeholder="Why hit 16 vs dealer 10?",
        height=80
    )
    
    if st.button("Ask Grok", type="primary"):
        if question.strip():
            with st.spinner("Thinking..."):
                try:
                    response = rag_chain.get_response(question)
                    st.info(response)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Enter a question!")
    
    # Quick examples
    with st.expander("💡 Examples"):
        st.markdown("""
        • Why hit 16 vs 10?  
        • When to double down?  
        • Hard vs soft hands?  
        • Why split 8s?
        """)

# Footer
st.markdown("---")
st.markdown("*Optimal blackjack strategy*")