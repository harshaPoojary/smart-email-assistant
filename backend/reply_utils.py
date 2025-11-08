# backend/reply_utils.py
import re

def generate_reply(email):
    """
    Generates a polite, context-aware reply draft (offline).
    Input: email dict with 'subject', 'sender', 'snippet'
    """
    subject = email.get("subject", "").lower()
    snippet = email.get("snippet", "").lower()
    sender = email.get("sender", "Someone")

    # Choose tone based on content
    if any(word in subject + snippet for word in ["job", "opportunity", "hiring", "position"]):
        reply = f"""Hello {sender.split('<')[0].strip()},

Thank you for reaching out about the job opportunity. 
I appreciate the information shared and would like to know more details about the role and next steps.

Kind regards,  
Harsha"""
    elif any(word in subject + snippet for word in ["course", "learn", "training", "skills"]):
        reply = f"""Hi {sender.split('<')[0].strip()},

Thank you for sharing this learning opportunity. 
I’ll take a closer look at the course content and see if it fits my goals.

Best,  
Harsha"""
    elif any(word in subject + snippet for word in ["offer", "discount", "promotion"]):
        reply = f"""Dear {sender.split('<')[0].strip()},

Thanks for informing me about the current offers. 
I’ll review the details and get back if I decide to proceed.

Warm regards,  
Harsha"""
    elif any(word in subject + snippet for word in ["astrology", "horoscope", "rahu", "planet"]):
        reply = f"""Hello {sender.split('<')[0].strip()},

Thank you for the astrology update. 
I’ll look into the recommendations and see if they align with my current interests.

Best wishes,  
Harsha"""
    else:
        reply = f"""Hello {sender.split('<')[0].strip()},

Thank you for your email. 
I’ve read through your message and will get back to you soon.

Best regards,  
Harsha"""

    return reply
