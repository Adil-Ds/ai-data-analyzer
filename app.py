import streamlit as st

st.set_page_config(page_title="AI Data Analyzer", layout="wide")

st.sidebar.title("🔎 AI Analyzer Menu")
st.sidebar.page_link("pages/1_Home.py", label="🏠 Home")
st.sidebar.page_link("pages/2_Upload_Analyze.py", label="📊 Upload & Analyze")
st.sidebar.page_link("pages/3_Pricing.py", label="💰 Pricing")
st.sidebar.page_link("pages/4_Login.py", label="🔐 Login / Signup")

st.markdown("# Welcome to AI Data Analyzer!")
st.write("Use the sidebar to navigate.")