# 📁 File: utils.py
import pandas as pd
import tempfile
import requests
from fpdf import FPDF
import plotly.express as px
from prophet import Prophet

import os
GROQ_API_KEY = os.environ.get("GROQ_API")

MODEL_NAME = "llama3-8b-8192"

def generate_pdf(insight_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14, style="B")
    pdf.cell(0, 10, "AI Analyzer", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    lines = insight_text.split("\n")
    for line in lines:
        if ":" in line:
            key, value = line.split(":", 1)
            pdf.set_font("Arial", style="B", size=12)
            pdf.multi_cell(0, 10, txt=key + ":")
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, txt=value.strip())
        else:
            pdf.multi_cell(0, 10, txt=line)
    temp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_path.name)
    return temp_path.name

def analyze_data(df, prompt):
    preview = df.head(5).to_csv(index=False)
    stats = df.describe().to_string()
    full_prompt = f"""You are a data analyst.\n\nDataset Preview:\n{preview}\n\nStatistics:\n{stats}\n\nUser prompt: {prompt}\n\nProvide structured and helpful data analysis.\n"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are a helpful data analyst."},
            {"role": "user", "content": full_prompt}
        ]
    }

    try:
        res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
        ai_response = res.json()['choices'][0]['message']['content']
    except Exception as e:
        ai_response = f"Groq API error: {e}"

    stats_md = df.describe().to_markdown()
    pdf_path = generate_pdf(ai_response)
    return ai_response, df.head().to_markdown(), stats_md, pdf_path

def infer_plot_type(prompt):
    prompt = prompt.lower()
    if any(kw in prompt for kw in ["trend", "time", "date", "over time", "daily", "monthly"]):
        return "line"
    elif any(kw in prompt for kw in ["compare", "versus", "highest", "top", "category"]):
        return "bar"
    elif any(kw in prompt for kw in ["distribution", "histogram", "frequency"]):
        return "histogram"
    elif any(kw in prompt for kw in ["share", "percentage", "portion", "pie"]):
        return "pie"
    else:
        return "bar"

def generate_plot(df, prompt):
    plot_type = infer_plot_type(prompt)
    num_cols = df.select_dtypes(include='number').columns.tolist()
    cat_cols = df.select_dtypes(include='object').columns.tolist()

    fig = None
    if plot_type == "line":
        date_cols = [col for col in df.columns if 'date' in col.lower() or pd.api.types.is_datetime64_any_dtype(df[col])]
        if date_cols and num_cols:
            df[date_cols[0]] = pd.to_datetime(df[date_cols[0]], errors='coerce')
            fig = px.line(df, x=date_cols[0], y=num_cols[0], title="Line Chart")
    elif plot_type == "bar" and cat_cols and num_cols:
        grouped = df.groupby(cat_cols[0])[num_cols[0]].sum().reset_index()
        fig = px.bar(grouped, x=cat_cols[0], y=num_cols[0], title="Bar Chart")
    elif plot_type == "histogram" and num_cols:
        fig = px.histogram(df, x=num_cols[0], title="Histogram")
    elif plot_type == "pie" and cat_cols and num_cols:
        grouped = df.groupby(cat_cols[0])[num_cols[0]].sum().reset_index()
        fig = px.pie(grouped, names=cat_cols[0], values=num_cols[0], title="Pie Chart")
    return fig
