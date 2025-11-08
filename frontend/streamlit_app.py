# frontend/streamlit_app.py

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

# --- Backend imports ---
sys.path.append(str(Path(__file__).resolve().parents[1] / "backend"))
from gmail_utils import fetch_unread_emails
from llm_utils import summarize_emails_extractive as summarize_emails
from reply_utils import generate_reply

# --- Page setup ---
st.set_page_config(page_title="Smart Email Assistant", page_icon="📧", layout="wide")

# --- Header / Intro ---
st.title("📧 Smart Email Assistant")
st.markdown("### 💡 AI-powered email summarizer & auto-reply generator — 100% free and local.")
st.markdown("Use the buttons below to fetch unread Gmail messages, summarize them, and generate polite replies automatically.")
st.divider()

# --- Custom CSS for modern dark theme ---
st.markdown("""
    <style>
    /* General app styling */
    body {
        background-color: #0e1117;
        color: #fafafa;
    }
    .stApp {
        background-color: #0e1117;
    }

    /* Titles */
    h1, h2, h3, h4 {
        color: #00c4ff !important;
    }

    /* Expander header */
    .streamlit-expanderHeader {
        font-weight: 600;
        color: #00c4ff !important;
    }

    /* Text area */
    textarea {
        background-color: #161b22 !important;
        color: #e0e0e0 !important;
        border-radius: 10px !important;
        font-size: 0.9rem !important;
    }

    /* Primary button */
    button[kind="primary"] {
        background-color: #00c4ff !important;
        color: black !important;
        border-radius: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)


# --- Step 1: Fetch unread emails ---
if st.button(" Fetch Unread Emails"):
    with st.spinner("Connecting to Gmail..."):
        emails = fetch_unread_emails()
    if not emails:
        st.warning("📭 No unread emails found.")
    else:
        st.success(f"✅ Fetched {len(emails)} unread emails.")
        st.session_state["emails"] = emails


# --- Step 2: Display summaries & replies ---
if "emails" in st.session_state:
    emails = st.session_state["emails"]

    if st.button(" Generate Summary"):
        with st.spinner("Summarizing emails..."):
            summary = summarize_emails(emails)
        st.text_area("Summary of Unread Emails", summary, height=250)

    st.write("---")
    st.subheader(" Individual Emails & Reply Suggestions")

    for i, email in enumerate(emails[:5]):
        with st.expander(f"📩 {email['subject']}"):
            st.write(f"**From:** {email['sender']}")
            st.write(f"**Snippet:** {email['snippet']}")
            reply = generate_reply(email)
            st.text_area(
                "💌 Suggested Reply Draft",
                reply,
                height=150,
                key=f"reply_{i}"
            )

    # --- Step 3: Download Replies as CSV ---
    reply_data = [
        {
            "Sender": email["sender"],
            "Subject": email["subject"],
            "Snippet": email["snippet"],
            "Suggested Reply": generate_reply(email),
        }
        for email in emails[:5]
    ]

    df = pd.DataFrame(reply_data)
    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download Replies as CSV",
        data=csv,
        file_name="smart_email_replies.csv",
        mime="text/csv",
    )
