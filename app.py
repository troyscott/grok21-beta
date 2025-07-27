import streamlit as st
from rag_chain import GrokRagChain

# Page configuration
st.set_page_config(
    page_title="Grok21",
    page_icon="🃏",
    layout="centered"
)

# Import from strategy_table.py
try:
    from strategy_table import get_action, get_action_text
except ImportError:
    # Fallback if strategy_table.py isn't available
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

    def get_action_text(action_code):
        """Convert action code to readable text"""
        actions = {
            'H': 'HIT',
            'S': 'STAND', 
            'D': 'DOUBLE DOWN',
            'P': 'SPLIT'
        }
        return actions.get(action_code, 'HIT')

def get_action_display(action_code):
    """Convert action code to display with icon and color"""
    actions = {
        'H': {'text': 'HIT', 'icon': '👊', 'color': '#ff6b6b', 'bg': '#2d1b1b'},
        'S': {'text': 'STAND', 'icon': '✋', 'color': '#51cf66', 'bg': '#1b2d1b'},
        'D': {'text': 'DOUBLE DOWN', 'icon': '⬆️', 'color': '#339af0', 'bg': '#1b1f2d'},
        'Ds': {'text': 'DOUBLE OR STAND', 'icon': '⬆️', 'color': '#339af0', 'bg': '#1b1f2d'},
        'P': {'text': 'SPLIT', 'icon': '✂️', 'color': '#ffa726', 'bg': '#2d241b'}
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

# Dark theme styling
st.markdown("""
<style>
/* Dark theme globals */
.stApp {
    background: #0e1117;
    color: #fafafa;
}

/* Main container */
.main .block-container {
    padding: 1rem;
    max-width: 600px;
    background: #1e1e1e;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    margin: 0.5rem auto;
    border: 1px solid #333;
}

/* Headers */
h1, h2, h3 {
    color: #fafafa !important;
}

/* Buttons */
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
    box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
}

.stButton > button:hover {
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    transform: translateY(-1px);
}

/* Input fields */
.stSelectbox > div > div {
    background: #2a2a2a;
    border: 2px solid #444;
    border-radius: 6px;
    color: #fafafa;
}

.stNumberInput > div > div > input {
    background: #2a2a2a;
    border: 2px solid #444;
    border-radius: 6px;
    color: #fafafa;
    font-size: 16px;
    height: 44px;
}

.stTextArea textarea {
    background: #2a2a2a;
    border: 2px solid #444;
    border-radius: 6px;
    color: #fafafa;
    font-size: 16px;
}

/* Card display */
.card-display {
    background: linear-gradient(135deg, #1a2332 0%, #2d1b69 100%);
    border-radius: 8px;
    padding: 1rem;
    margin: 1rem 0;
    text-align: center;
    border: 1px solid #444;
}

.big-cards {
    font-size: 2rem;
    margin: 0.5rem;
    color: #fafafa;
}

/* Action result */
.action-result {
    border-radius: 12px;
    padding: 2rem;
    text-align: center;
    font-size: 1.5rem;
    font-weight: 700;
    margin: 1rem 0;
    border: 2px solid;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}

/* BIGGER TABS - This is the key fix! */
.stTabs [data-baseweb="tab-list"] {
    background: #2a2a2a;
    border-radius: 10px;
    padding: 8px;
    gap: 8px;
}

.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #fafafa;
    border-radius: 8px;
    padding: 16px 32px !important;
    font-size: 18px !important;
    font-weight: 600 !important;
    min-height: 56px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    border: 2px solid transparent;
    transition: all 0.3s ease;
}

.stTabs [data-baseweb="tab"]:hover {
    background: #3a3a3a;
    border-color: #667eea;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border-color: #667eea;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

/* Tab content */
.stTabs [data-baseweb="tab-panel"] {
    padding-top: 24px;
}

/* Expander */
.streamlit-expanderHeader {
    background: #2a2a2a;
    color: #fafafa;
    border-radius: 6px;
}

.streamlit-expanderContent {
    background: #1e1e1e;
    border: 1px solid #444;
    border-radius: 6px;
}

/* Info boxes */
.stInfo {
    background: #1a2332;
    border-left: 4px solid #339af0;
    color: #fafafa;
}

.stSuccess {
    background: #1b2d1b;
    border-left: 4px solid #51cf66;
    color: #fafafa;
}

.stWarning {
    background: #2d241b;
    border-left: 4px solid #ffa726;
    color: #fafafa;
}

.stError {
    background: #2d1b1b;
    border-left: 4px solid #ff6b6b;
    color: #fafafa;
}

/* Spinner */
.stSpinner > div {
    color: #667eea;
}

/* Sidebar (if used) */
.css-1d391kg {
    background: #1e1e1e;
}

/* Mobile responsiveness */
@media (max-width: 768px) {
    .main .block-container {
        padding: 0.8rem;
        margin: 0.2rem;
        border-radius: 8px;
    }
    
    .card-display {
        padding: 0.8rem;
    }
    
    .action-result {
        padding: 1rem;
        font-size: 1.1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 12px 20px !important;
        font-size: 16px !important;
        min-height: 48px !important;
    }
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
    # Hand type explanation
    with st.expander("ℹ️ Hand Types Quick Guide"):
        st.markdown("""
        **🃏 Hard Hand**: No Ace OR Ace counts as 1  
        Examples: 10+6=16, 8+5=13, A+7+9=17
        
        **♥️ Soft Hand**: Ace counts as 11  
        Examples: A+6=17 (soft), A+2+4=17 (soft)
        
        **👥 Pair**: Two identical cards  
        Examples: 8+8, A+A, K+K
        """)
    
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
    
    # Hand type hint based on selection
    if hand_type == "hard":
        st.info("💡 **Hard Hand**: No usable Ace (A+6+5=12, not 22)")
    elif hand_type == "soft":
        st.info("💡 **Soft Hand**: Ace counts as 11 (A+6=17)")
    else:
        st.info("💡 **Pair**: Two identical cards (8+8, A+A)")
    
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