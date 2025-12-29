import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="ArthaFlow | Personal Finance Hub",
    page_icon="🌊",
    layout="centered"
)

# 2. Custom CSS for Fintech Look & Dark Blue Hover
st.markdown("""
    <style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Main Button Styling */
    div.stButton > button {
        width: 100%;
        border-radius: 10px;
        height: 3.5em;
        background-color: #007bff; /* Primary Blue */
        color: white;
        border: none;
        font-size: 18px;
        font-weight: 700;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    /* Hover State: Darker Blue */
    div.stButton > button:hover {
        background-color: #004a99; /* Darker Blue */
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Click Effect */
    div.stButton > button:active {
        background-color: #003366;
        transform: translateY(0px);
    }

    /* Card Styling */
    .finance-card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #e0e0e0;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Header Section
st.title("🌊 ArthaFlow")
st.markdown("#### *Master Your Money, Secure Your Future.*")
st.write("Welcome to the ArthaFlow ecosystem. Please select a module below to begin your financial analysis.")

st.divider()

# 4. Interactive Navigation Grid
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("### 📈 SIP Planner")
    st.write("Visualize the growth of your investments over time using the power of compounding.")
    # Ensure SIP_Planner.py is directly inside the 'pages' folder
    if st.button("Start Planning →", key="sip_btn"):
        st.switch_page("pages/SIP_Planner.py")

with col2:
    st.markdown("### 🏠 Loan Analyser")
    st.write("Deep dive into your debt. Calculate EMIs and see how much interest you can save.")
    # Ensure loan_analyzer.py is directly inside the 'pages' folder
    if st.button("Start Analysing →", key="loan_btn"):
        st.switch_page("pages/Loan_Analyzer.py")

# 5. Footer Info
st.divider()
with st.expander("ℹ️ About ArthaFlow"):
    st.write("""
        ArthaFlow is designed to give you clarity on your personal finances. 
        Whether you are investing for the future or managing current debt, 
        our tools provide data-driven insights to help you make better decisions.
    """)

st.caption("© 2025 ArthaFlow | Built for Financial Clarity")