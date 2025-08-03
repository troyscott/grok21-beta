import streamlit as st
from rag_chain import GrokRagChain

# Page configuration
st.set_page_config(
    page_title="Grok21 - Beta",
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
        # For pairs, the total represents two identical cards
        # So the individual card value is total ÷ 2
        card_value = total // 2
        if card_value < 2 or card_value > 11:
            # Invalid pair - fallback to hard hand display
            if total <= 11:
                first, second = max(2, total - 2), 2
            else:
                first, second = 10, total - 10
            return [display_card(first, "♠"), display_card(second, "♣")]
        return [display_card(card_value, "♠"), display_card(card_value, "♣")]
    elif hand_type == "soft":
        other_value = total - 11
        if other_value < 1:
            other_value = 1
        return [display_card(11, "♥"), display_card(other_value, "♠")]
    else:  # hard
        if total <= 11:
            first, second = max(2, total - 2), 2
        else:
            first, second = 10, total - 10
        return [display_card(first, "♠"), display_card(second, "♣")]

# Dark theme styling with ANIMATIONS!
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
    transition: all 0.3s ease;
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

/* ANIMATED ACTION RESULT! */
.action-result {
    border-radius: 12px;
    padding: 2rem;
    text-align: center;
    font-size: 1.5rem;
    font-weight: 700;
    margin: 1rem 0;
    border: 2px solid;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    
    /* Entry Animation */
    animation: actionEntry 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    position: relative;
    overflow: hidden;
}

/* Action entry animation */
@keyframes actionEntry {
    0% {
        opacity: 0;
        transform: scale(0.8) translateY(30px);
        box-shadow: 0 0 0 rgba(0,0,0,0);
    }
    50% {
        transform: scale(1.05) translateY(-5px);
    }
    100% {
        opacity: 1;
        transform: scale(1) translateY(0);
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
}

/* Animated icon */
.action-icon {
    animation: iconBounce 0.8s ease-out 0.3s;
    display: inline-block;
}

@keyframes iconBounce {
    0% { transform: scale(0.3) rotate(-10deg); }
    50% { transform: scale(1.2) rotate(5deg); }
    70% { transform: scale(0.9) rotate(-2deg); }
    100% { transform: scale(1) rotate(0deg); }
}

/* Pulsing glow effect */
.action-result::before {
    content: '';
    position: absolute;
    top: -2px;
    left: -2px;
    right: -2px;
    bottom: -2px;
    background: inherit;
    border-radius: 12px;
    z-index: -1;
    animation: pulseGlow 2s ease-in-out infinite;
    opacity: 0.7;
}

@keyframes pulseGlow {
    0%, 100% { 
        transform: scale(1);
        opacity: 0.7;
    }
    50% { 
        transform: scale(1.02);
        opacity: 0.9;
    }
}

/* Action text slide-in */
.action-text {
    animation: textSlide 0.5s ease-out 0.4s both;
}

@keyframes textSlide {
    0% {
        opacity: 0;
        transform: translateX(-20px);
    }
    100% {
        opacity: 1;
        transform: translateX(0);
    }
}

/* Special animations for different actions */
.hit-action {
    animation: actionEntry 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275), 
               hitShake 0.5s ease-in-out 0.8s;
}

@keyframes hitShake {
    0%, 100% { transform: translateX(0); }
    25% { transform: translateX(-3px); }
    75% { transform: translateX(3px); }
}

.stand-action {
    animation: actionEntry 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275),
               standSolid 0.4s ease-out 0.8s;
}

@keyframes standSolid {
    0% { transform: scale(1); }
    50% { transform: scale(1.02); }
    100% { transform: scale(1); }
}

.double-action {
    animation: actionEntry 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275),
               doubleUp 0.6s ease-out 0.8s;
}

@keyframes doubleUp {
    0% { transform: translateY(0); }
    50% { transform: translateY(-8px); }
    100% { transform: translateY(0); }
}

.split-action {
    animation: actionEntry 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275),
               splitMove 0.8s ease-out 0.8s;
}

@keyframes splitMove {
    0% { transform: scaleX(1); }
    25% { transform: scaleX(0.95); }
    50% { transform: scaleX(1.1); }
    100% { transform: scaleX(1); }
}

/* BIGGER TABS */
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

# Import the ask_grok_question function
from blackjack_game import ask_grok_question

# In your tabs or wherever you want the Grok interface:
tab1, tab2 = st.tabs(["Strategy Helper", "Ask Grok"])

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
            
            # Get action-specific CSS class
            action_class = f"{action_code.lower()}-action" if action_code in ['H', 'S', 'D', 'P'] else "action-result"
            
            # Display result with ANIMATED styling and icon
            st.markdown(f"""
            <div class="action-result {action_class}" style="
                color: {action_info['color']}; 
                background-color: {action_info['bg']};
                border-color: {action_info['color']};
            ">
                <div class="action-icon" style="font-size: 2rem; margin-bottom: 0.5rem;">
                    {action_info['icon']}
                </div>
                <div class="action-text">
                    {action_info['text']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error: {e}")

with tab2:
    st.header("🤖 Ask Grok About Blackjack Strategy")
    st.markdown("Get detailed explanations about blackjack strategy decisions and rules.")
    
    question = st.text_area(
        "Your question:",
        height=100,
        placeholder="E.g., Why should I hit on 16 against dealer's 10?",
        help="Ask about specific hands, general strategy, or blackjack rules"
    )
    
    if st.button("🤖 Ask Grok", type="primary"):
        if question and question.strip():
            with st.spinner('🤖 Asking Grok... This may take a few seconds.'):
                response = ask_grok_question(question)
            
            st.markdown("---")
            st.markdown("### 🤖 Grok's Response:")
            st.markdown(response)
            
            with st.expander("📝 Your Question"):
                st.markdown(f"*{question}*")
        else:
            st.warning("Please enter a question first.")

# Footer
st.markdown("---")
st.markdown("*Optimal blackjack strategy*")