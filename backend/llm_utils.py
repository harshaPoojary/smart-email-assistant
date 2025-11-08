# backend/llm_utils.py
from typing import List, Dict
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
import textwrap

def summarize_emails_extractive(emails: List[Dict], sentences_per_email: int = 2) -> str:
    """
    Extractive summarization using LexRank (sumy).
    emails: list of dicts with keys 'subject', 'sender', 'snippet'
    Returns a readable bullet-point summary string.
    """
    if not emails:
        return "📭 No unread emails to summarize."

    bullets = []
    for e in emails:
        # Build short text from subject + snippet
        subj = e.get("subject", "(No subject)")
        sender = e.get("sender", "(Unknown)")
        snippet = e.get("snippet", "")
        # Combine into a small document for extractive summarization
        doc_text = f"Subject: {subj}\nFrom: {sender}\n\n{snippet}"
        # Use sumy to get top sentences
        parser = PlaintextParser.from_string(doc_text, Tokenizer("english"))
        summarizer = LexRankSummarizer()
        # Limit sentences to avoid huge output
        summary_sentences = summarizer(parser.document, sentences_per_email)
        # Join the sentences into one short line
        summary_line = " ".join(str(s).strip() for s in summary_sentences)
        # Fallback if summary empty
        if not summary_line:
            # Use the first 120 chars of snippet
            summary_line = (snippet[:120] + "...") if snippet else "(no content available)"
        # Create bullet
        bullet = f"- {sender.split('<')[0].strip()}: {subj} — {summary_line}"
        bullets.append(bullet)

    header = f"📧 {len(emails)} Unread Emails — Extractive Summary:\n"
    return header + "\n".join(textwrap.fill(b, width=100) for b in bullets)
