import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import streamlit as st
import pandas as pd
import json
import io
from datetime import datetime
from ai.gpt_explainer import explain_filing
from ai.gpt_explainer import explain_filing

# -----------------------------
# 📁 File Config
# -----------------------------
DATA_FILE = "data/filing_schedule.json"

def load_filings():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_filings(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# -----------------------------
# 🧠 Helper Functions
# -----------------------------
def get_days_left(due_date):
    due = pd.to_datetime(due_date)
    today = pd.Timestamp.now().normalize()
    return (due - today).days

def urgency_badge(days_left):
    if days_left < 0:
        return "🔴 Overdue"
    elif days_left == 0:
        return "🟠 Due today"
    elif days_left <= 3:
        return f"🟡 {days_left} day(s) left"
    elif days_left <= 7:
        return f"🔵 {days_left} days left"
    else:
        return f"🟢 {days_left} days left"

def convert_to_csv(data):
    df = pd.DataFrame(data)
    return df.to_csv(index=False).encode("utf-8")

# -----------------------------
# 🚀 Main UI
# -----------------------------
st.set_page_config("Compliance Tracker", page_icon="📅", layout="wide")

st.title("📅 Compliance Filing Tracker")
st.markdown("Keep your team ahead of critical regulatory and tax deadlines.")

filings = load_filings()

# -----------------------------
# ⬇️ CSV Export
# -----------------------------
if st.button("⬇️ Export All Filings to CSV"):
    csv = convert_to_csv(filings)
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="compliance_filings.csv",
        mime="text/csv"
    )

# -----------------------------
# ✅ Show Completed Toggle
# -----------------------------
show_completed = st.checkbox("✅ Show completed filings", value=False)
pending, completed = [], []

for filing in sorted(filings, key=lambda x: x["due_date"]):
    if filing["completed"]:
        completed.append(filing)
    else:
        pending.append(filing)

# -----------------------------
# 🔄 Filing Card Renderer
# -----------------------------
def render_filing_card(filing, index):
    days_left = get_days_left(filing["due_date"])
    badge = urgency_badge(days_left)

    with st.container():
        col1, col2 = st.columns([7, 1])
        with col1:
            st.markdown(f"### {filing['filing_name']}")
            st.markdown(f"**📂 Filing Type:** `{filing.get('filing_type', 'N/A')}`")
            st.markdown(f"📝 *{filing.get('description', 'No description provided.')}*")
            st.markdown(f"""
- 🗓️ **Due Date:** `{filing['due_date']}`
- 🌍 **Jurisdiction:** `{filing['jurisdiction']}`
- 🏢 **Business Type:** `{filing['business_type']}`
- 📧 **Escalation Contact:** `{filing['escalation_contact']}`
- ⏱️ **Status:** {badge}
""")

            with st.expander("💡 What does this filing mean?"):
                if st.button(f"Explain '{filing['filing_name']}'", key=f"explain-{index}"):
                    with st.spinner("Explaining..."):
                        try:
                            explanation = explain_filing(
                                filing['filing_name'],
                                filing.get('filing_type', 'General'),
                                filing['jurisdiction']
                            )
                            st.success(explanation)
                        except Exception as e:
                            st.error("❌ Unable to generate explanation. Check your API key or internet connection.")

        with col2:
            checked = st.checkbox("Mark as Done", value=filing["completed"], key=filing["filing_name"])
            filings[index]["completed"] = checked

# -----------------------------
# 📌 Show Pending Filings
# -----------------------------
if pending:
    st.subheader("🕗 Pending Filings")
    for i, filing in enumerate(filings):
        if not filing["completed"]:
            render_filing_card(filing, i)
else:
    st.success("🎉 All filings are complete!")

# -----------------------------
# 📌 Show Completed Filings (Optional)
# -----------------------------
if show_completed and completed:
    st.subheader("✅ Completed Filings")
    for i, filing in enumerate(filings):
        if filing["completed"]:
            render_filing_card(filing, i)

# -----------------------------
# 💾 Save Changes
# -----------------------------
save_filings(filings)
