import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- INDIAN CURRENCY FORMATTER ---
def format_indian(number):
    s = f"{round(number):,}"
    parts = s.split(",")
    if len(parts) <= 2: return "₹ " + s
    else:
        last_three = parts[-1]
        other_parts = "".join(parts[:-1])
        res = ""
        n = len(other_parts)
        for i in range(n):
            if i > 0 and (n - i) % 2 == 0: res += ","
            res += other_parts[i]
        return "₹ " + res + "," + last_three

st.set_page_config(page_title="Loan Step-Up Planner", layout="wide")

# --- SIDEBAR: THE EDUCATION HUB ---
with st.sidebar:
    st.title("📖 Strategy Guide")
    st.markdown("""
    ### How to use this tool:
    1. **Red Line:** Your remaining loan debt.
    2. **Green Line:** Your growing SIP wealth.
    3. **The Goal:** Find the **'Intersection Point'** where green crosses red. That is your "Freedom Date."
    
    ---
    
    ### 🚀 The Step-Up Advantage
    A **Step-Up** means increasing your ₹10,000 contribution by a fixed % every year as your salary increases.
    
    * **Why it's a 'Cheat Code':** Inflation usually increases your salary by 7-10%. By 'stepping up' your loan contribution by the same amount, you don't feel the pinch, but the bank feels the heat!
    * **Impact:** A 10% annual step-up can often clear a 15-year loan in just **6-7 years** total.
    
    ---
    
    ### 💡 The 3 Pillars of Closure:
    
    * **The Power of 8% vs 12%**: Your loan costs 8%, but your SIP earns ~12%. You are "profiting" on the 4% difference.
    * **Prepayment Impact**: Every ₹1 extra paid today saves you ~₹2.5 in future interest.
    * **The 'Kill Switch'**: When the lines cross, you can withdraw your SIP and pay off the bank in one shot.
    
    ---
    ### 🛠 Tips for Success:
    * **Choice 1 (70:30):** Better for "Peace of Mind" as the loan drops very fast.
    * **Choice 2 (50:50):** Best for "Wealth Building" and emergency liquidity.
    """)
    st.warning("Note: The Step-Up applies to your extra contribution (₹10k), not the bank's base EMI.")

# --- MAIN AREA ---
st.title("🏠 Home Loan 'Step-Up' Strategy Planner")

# Section 1: Inputs
with st.container():
    st.subheader("1. Loan & Contribution Setup")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        loan_bal = st.number_input("Current Balance (₹)", value=2225354)
        rate = st.slider("Interest Rate (%)", 7.0, 12.0, 8.1)
    with col2:
        emi = st.number_input("Monthly EMI (₹)", value=21047)
        sip_return = st.slider("SIP Return (%)", 8.0, 18.0, 12.0)
    with col3:
        initial_cont = st.number_input("Initial Monthly Contribution (₹)", value=10000)
        step_up_pct = st.slider("Annual Step-Up (%)", 0, 20, 10)
    with col4:
        split_ratio = st.select_slider("Split (Prepay% : SIP%)", options=[0, 20, 40, 50, 60, 80, 100], value=50)

# Calculations
def get_stepup_data():
    data = []
    curr_loan, curr_sip = loan_bal, 0
    current_monthly_cont = initial_cont
    intersect_m = None
    
    for m in range(1, 241):
        # Annual Step-Up Logic: Every 12 months, increase the contribution
        if m > 1 and (m - 1) % 12 == 0:
            current_monthly_cont *= (1 + (step_up_pct / 100))
        
        m_prepay = (current_monthly_cont * split_ratio) / 100
        m_sip = current_monthly_cont - m_prepay
        
        # Loan Math
        interest = curr_loan * (rate / 100 / 12)
        principal = (emi - interest) + m_prepay
        curr_loan = max(0, curr_loan - principal)
        
        # SIP Math
        curr_sip = (curr_sip + m_sip) * (1 + (sip_return / 100 / 12))
        
        data.append({"Month": m, "Loan": curr_loan, "SIP": curr_sip, "Monthly_Cont": current_monthly_cont})
        
        if curr_sip >= curr_loan and intersect_m is None and curr_loan > 0:
            intersect_m = m
            
    return pd.DataFrame(data), intersect_m

df, intersect = get_stepup_data()

# Section 2: Visual Results
st.markdown("---")
r1, r2, r3 = st.columns(3)
if intersect:
    r1.metric("Freedom Date", f"{intersect // 12}y {intersect % 12}m")
    r2.metric("Final SIP Value", format_indian(df.iloc[intersect-1]['SIP']))
    # Calculating end contribution to show growth
    end_cont = df.iloc[intersect-1]['Monthly_Cont']
    r3.metric("Final Monthly Contribution", format_indian(end_cont))

# The Visualization
fig = go.Figure()
fig.add_trace(go.Scatter(x=df['Month'], y=df['Loan'], name="Debt (Loan)", line=dict(color='#FF4B4B', width=3)))
fig.add_trace(go.Scatter(x=df['Month'], y=df['SIP'], name="Wealth (SIP)", line=dict(color='#00CC96', width=3)))
if intersect:
    fig.add_vline(x=intersect, line_dash="dash", line_color="orange")

fig.update_layout(title="The Impact of Stepping Up Your Contribution", hovermode="x unified")
st.plotly_chart(fig, use_container_width=True)

# Data Table
with st.expander("View Month-by-Month Growth & Step-Up Schedule"):
    st.dataframe(df.style.format({
        "Loan": lambda x: format_indian(x),
        "SIP": lambda x: format_indian(x),
        "Monthly_Cont": lambda x: format_indian(x)
    }))