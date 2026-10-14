"""Simple local results-query demo. This is not a GenAI/Bedrock chatbot."""
from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Healthcare Fraud Results", page_icon="🔎")
st.title("Healthcare Claim Fraud Results")
st.caption("Prototype interface for querying model output; suspicious means review required, not proven fraud.")

csv_path = Path("outputs/fraud_results.csv")
if not csv_path.exists():
    st.warning("No results file found. Place fraud_results.csv in outputs/ or update the path in this app.")
    st.stop()

df = pd.read_csv(csv_path)
st.write(f"Loaded **{len(df)}** claim records.")
status_col = "fraud_status"
if status_col not in df.columns:
    st.error("The results file needs a 'fraud_status' column.")
    st.stop()

query = st.text_input("Ask a question", placeholder="e.g. show suspicious claims")
if query:
    q = query.lower()
    if any(word in q for word in ["suspicious", "fraud", "abnormal"]):
        result = df[df[status_col].astype(str).str.lower().isin(["suspicious", "fraud", "1", "-1"])]
        st.write(f"Found **{len(result)}** records marked suspicious by the model.")
        st.dataframe(result, use_container_width=True)
    elif "normal" in q:
        result = df[df[status_col].astype(str).str.lower().eq("normal")]
        st.write(f"Found **{len(result)}** records marked normal.")
        st.dataframe(result, use_container_width=True)
    elif "count" in q or "how many" in q or "summary" in q:
        st.dataframe(df[status_col].value_counts().rename_axis("status").reset_index(name="count"))
    else:
        st.info("Try asking: 'show suspicious claims', 'show normal claims', or 'give summary'.")

with st.expander("Show all results"):
    st.dataframe(df, use_container_width=True)
