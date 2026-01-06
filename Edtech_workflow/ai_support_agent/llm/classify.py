
# Email Classification Engine

from config.settings import (
    SUPPORT_CATEGORIES,
    HIGH_URGENCY_KEYWORDS,
    MEDIUM_URGENCY_KEYWORDS,
    POSITIVE_KEYWORDS,
    NEGATIVE_KEYWORDS
)

class EmailClassifier:
    """Classifies support emails into categories and determines urgency/sentiment"""
    
    def __init__(self):
        """Initialize the classifier"""
        self.categories = SUPPORT_CATEGORIES
        print("✅ EmailClassifier initialized")
    
    def classify(self, subject: str, body: str) -> dict:
        """
        Classify an email
        
        Args:
            subject (str): Email subject
            body (str): Email body
            
        Returns:
            dict: Classification results
        """
        text = f"{subject} {body}".lower()
        
        # Determine category
        category = self._classify_category(text)
        
        # Determine sub-category
        sub_category = self._classify_sub_category(category, text)
        
        # Determine urgency
        urgency = self._classify_urgency(text)
        
        # Determine sentiment
        sentiment = self._classify_sentiment(text)
        
        # Calculate confidence
        confidence = self._calculate_confidence(text, category)
        
        # Determine if escalation needed
        escalate_to_human = urgency == "High" or confidence < 0.5
        
        return {
            "category": category,
            "sub_category": sub_category,
            "urgency": urgency,
            "sentiment": sentiment,
            "confidence": confidence,
            "escalate_to_human": escalate_to_human
        }
    
    def _classify_category(self, text: str) -> str:
        """Classify into main category"""
        text_lower = text.lower()
        
        # Payment & Billing keywords
        if any(word in text_lower for word in ["refund", "payment", "billing", "invoice", "price", "cost", "charged"]):
            return "Payment & Billing"
        
        # Technical Issues keywords
        if any(word in text_lower for word in ["cannot access", "login", "error", "broken", "not working", "video", "playback", "platform"]):
            return "Technical Issues"
        
        # Course Content keywords
        if any(word in text_lower for word in ["certificate", "completion", "course", "material", "content", "curriculum"]):
            return "Course Content"
        
        # Account Management keywords
        if any(word in text_lower for word in ["password", "account", "profile", "email", "delete", "two factor", "verification"]):
            return "Account Management"
        
        # Default
        return "General Queries"
    
    def _classify_sub_category(self, category: str, text: str) -> str:
        """Classify into sub-category"""
        text_lower = text.lower()
        
        if category not in self.categories:
            return "Unknown"
        
        sub_categories = self.categories[category]["sub_categories"]
        
        # Map keywords to sub-categories
        mapping = {
            "Technical Issues": {
                "Platform Access": ["cannot access", "access denied", "login"],
                "Video Playback": ["video", "playback", "cannot play"],
                "Course Materials": ["materials", "content", "download"],
                "Account Login": ["login", "password", "sign in"],
                "Browser Compatibility": ["browser", "chrome", "firefox", "safari"]
            },
            "Payment & Billing": {
                "Refund Request": ["refund", "return", "money back"],
                "Payment Failed": ["payment failed", "charge", "declined"],
                "Invoice": ["invoice", "receipt", "bill"],
                "Subscription": ["subscription", "renew", "cancel"],
                "Course Pricing": ["price", "cost", "expensive"]
            },
            "Course Content": {
                "Course Completion": ["completion", "finished", "done"],
                "Certificate": ["certificate", "proof", "credential"],
                "Curriculum": ["curriculum", "course structure"],
                "Course Duration": ["duration", "long", "hours"],
                "Content Quality": ["quality", "content", "material"]
            },
            "Account Management": {
                "Profile Update": ["profile", "update", "change"],
                "Password Reset": ["password", "reset", "forgot"],
                "Account Deletion": ["delete", "remove", "cancel account"],
                "Email Change": ["email", "change email"],
                "Two Factor Auth": ["2fa", "two factor", "authentication"]
            }
        }
        
        if category in mapping:
            for sub_cat, keywords in mapping[category].items():
                if any(keyword in text_lower for keyword in keywords):
                    return sub_cat
        
        return sub_categories[0] if sub_categories else "Unknown"
    
    def _classify_urgency(self, text: str) -> str:
        """Classify urgency level"""
        text_lower = text.lower()
        
        # High urgency
        if any(word in text_lower for word in HIGH_URGENCY_KEYWORDS):
            return "High"
        
        # Medium urgency
        if any(word in text_lower for word in MEDIUM_URGENCY_KEYWORDS):
            return "Medium"
        
        return "Low"
    
    def _classify_sentiment(self, text: str) -> str:
        """Classify sentiment"""
        text_lower = text.lower()
        
        positive_count = sum(1 for word in POSITIVE_KEYWORDS if word in text_lower)
        negative_count = sum(1 for word in NEGATIVE_KEYWORDS if word in text_lower)
        
        if positive_count > negative_count:
            return "Positive"
        elif negative_count > positive_count:
            return "Negative"
        else:
            return "Neutral"
    
    def _calculate_confidence(self, text: str, category: str) -> float:
        """Calculate classification confidence (0.0 to 1.0)"""
        # Base confidence
        confidence = 0.7
        
        # Increase confidence for specific categories
        if category != "General Queries":
            confidence += 0.15
        
        # Increase confidence for longer text
        if len(text) > 100:
            confidence += 0.1
        elif len(text) > 50:
            confidence += 0.05
        
        # Cap at 1.0
        return min(confidence, 1.0)