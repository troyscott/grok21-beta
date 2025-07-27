import streamlit as st
from blackjack_game import get_strategy_advice

# This is a simplified version of the app.py file that focuses on the "Get Strategy" button functionality

def main():
    st.title("Test Blackjack Strategy Advice")
    
    # Input fields
    player_total = st.number_input("Hand Total", min_value=5, max_value=21, value=12)
    dealer_upcard = st.selectbox("Dealer Upcard", options=[2, 3, 4, 5, 6, 7, 8, 9, 10, 11], index=8)
    hand_type = st.selectbox("Hand Type", options=["hard", "soft", "pair"])
    
    # Button
    get_advice = st.button("Get Strategy")
    
    # Display advice when button is clicked
    if get_advice:
        with st.spinner("Getting optimal strategy..."):
            advice = get_strategy_advice(player_total, dealer_upcard, hand_type)
            
            # Print the advice to the console for debugging
            print(f"Advice: {advice}")
            print(f"Type: {type(advice)}")
            
            # Display the advice using st.write (no HTML)
            st.write("Using st.write:")
            st.write(advice)
            
            # Display the advice using st.markdown (with HTML)
            st.write("Using st.markdown with HTML:")
            st.markdown(f"""
            <div style="padding: 1rem; border-radius: 8px; background-color: #f8f9fa; border-left: 4px solid #007bff; margin: 1rem 0;">
                <strong>Recommendation:</strong><br>
                {advice}
            </div>
            """, unsafe_allow_html=True)
            
            # Display the advice using st.markdown (without HTML)
            st.write("Using st.markdown without HTML:")
            st.markdown(advice)

if __name__ == "__main__":
    main()