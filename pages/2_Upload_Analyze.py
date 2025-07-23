import streamlit as st
import pandas as pd
from utils import analyze_data, generate_pdf, generate_plot

st.title("📊 Upload & Analyze")

uploaded_file = st.file_uploader("Upload CSV or Excel", type=["csv", "xls", "xlsx"])
prompt = st.text_input("Enter your analysis prompt", value="Show important insights")

if uploaded_file and prompt:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)

    with st.expander("Preview Data"):
        st.dataframe(df.head())

    if st.button("🔍 Analyze"):
        insights, preview, stats, pdf_path = analyze_data(df, prompt)
        st.subheader("🧠 AI Insight")
        st.markdown(insights)

        st.subheader("📄 Summary Stats")
        st.markdown(stats)

        st.subheader("📈 Auto Chart")
        fig = generate_plot(df, prompt)
        st.plotly_chart(fig)

        st.download_button("Download PDF", data=open(pdf_path, "rb"), file_name="insight.pdf")
