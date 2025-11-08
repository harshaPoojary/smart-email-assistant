#  Smart Email Assistant

###  AI-Powered Gmail Summarizer & Auto-Reply Generator  
_A completely free and local tool that connects to your Gmail inbox, summarizes unread emails, and generates polite, professional reply drafts automatically._

---

##  Features

 **Gmail Integration (OAuth 2.0)**
- Secure login using your Google account.
- Automatically fetches unread emails from your inbox.

 **Offline Summarization (No API Key Needed)**
- Uses the LexRank algorithm via the `sumy` NLP library.
- Works **offline** — no API costs or rate limits.

 **Auto-Reply Generator**
- Context-aware polite email replies powered by templates.
- Customizable drafts for each email.

 **Interactive Dashboard**
- Built with **Streamlit**.
- Clean **dark theme UI** with expandable cards for each email.
- Download all replies as a **CSV file**.

---

##  Tech Stack

| Layer | Technology |
|-------|-------------|
|  AI/NLP | Python, Sumy (LexRank Summarizer) |
|  Email Integration | Gmail API (OAuth 2.0) |
|  Frontend | Streamlit |
|  Backend | Python 3.11+, Google API Client |
|  Styling | Custom CSS (Dark Mode, Modern UI) |

---

##  Setup Instructions

### 1️⃣ Clone the Project
```bash
git clone https://github.com/<your-username>/smart-email-assistant.git
cd smart-email-assistant
 
