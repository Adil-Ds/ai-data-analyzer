import streamlit as st

st.title("💰 Pricing Plans")

plans = {
    "Free": {"Uploads": "2/month", "Forecasting": "❌", "Support": "Community"},
    "Plus": {"Uploads": "10/month", "Forecasting": "✅", "Support": "Email"},
    "Premium": {"Uploads": "Unlimited", "Forecasting": "✅", "Support": "Priority"}
}

for plan, features in plans.items():
    st.subheader(plan)
    for key, val in features.items():
        st.write(f"**{key}**: {val}")
    st.button(f"Subscribe to {plan}")
