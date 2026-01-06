# config/settings.py
# Configuration and Support Categories
import os

# 🔑 Groq API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ⚙️ Reply generation config
REPLY_CONFIG = {
    "model": "llama-3.1-8b-instant",
    "temperature": 0.3,
    "max_tokens": 300,
}

SUPPORT_CATEGORIES = {
    "Technical Issues": {
        "sub_categories": [
            "Platform Access",
            "Video Playback",
            "Course Materials",
            "Account Login",
            "Browser Compatibility"
        ]
    },
    "Payment & Billing": {
        "sub_categories": [
            "Refund Request",
            "Payment Failed",
            "Invoice",
            "Subscription",
            "Course Pricing"
        ]
    },
    "Course Content": {
        "sub_categories": [
            "Course Completion",
            "Certificate",
            "Curriculum",
            "Course Duration",
            "Content Quality"
        ]
    },
    "Account Management": {
        "sub_categories": [
            "Profile Update",
            "Password Reset",
            "Account Deletion",
            "Email Change",
            "Two Factor Auth"
        ]
    },
    "General Queries": {
        "sub_categories": [
            "Inquiry",
            "Suggestion",
            "Feedback",
            "Other"
        ]
    }
}

# Legal keywords - trigger immediate escalation
LEGAL_KEYWORDS = [
    "legal", "lawsuit", "attorney", "lawyer", 
    "compliance", "court", "dispute", "contract"
]

# Refund keywords - trigger immediate escalation
REFUND_KEYWORDS = [
    "refund", "money back", "reimbursement", "return", 
    "charge back", "refund request", "cancel subscription",
    "get my money back", "refund my payment"
]

# Escalation thresholds for business rules
ESCALATION_THRESHOLDS = {
    "repeated_contact_count": 2,  # Escalate if customer contacted 2+ times
    "high_confidence_threshold": 0.90,  # 90% confidence for high urgency escalation
    "medium_confidence_threshold": 0.85,  # 85% confidence for medium urgency escalation
    "low_confidence_threshold": 0.75,  # Below this = give benefit of doubt
}

# Urgency keywords
HIGH_URGENCY_KEYWORDS = [
    "urgent", "asap", "immediately", "critical", "emergency",
    "cannot access", "broken", "not working", "error", "failed"
]

MEDIUM_URGENCY_KEYWORDS = [
    "important", "soon", "need", "issue", "problem", "help"
]

# Sentiment keywords
POSITIVE_KEYWORDS = [
    "great", "excellent", "amazing", "love", "perfect", "wonderful",
    "thank you", "thanks", "appreciate", "satisfied"
]

NEGATIVE_KEYWORDS = [
    "bad", "terrible", "awful", "hate", "worst", "problem",
    "issue", "broken", "error", "frustrated", "angry"
]