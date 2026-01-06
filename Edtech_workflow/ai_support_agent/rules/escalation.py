# rules/escalation.py
# Business logic for ticket escalation - IMPROVED VERSION
# Now includes confidence thresholds and nuanced rules

from config.settings import (
    LEGAL_KEYWORDS,
    REFUND_KEYWORDS,
    ESCALATION_THRESHOLDS
)

class EscalationRules:
    """Centralized escalation logic with business rules - IMPROVED"""
    
    @staticmethod
    def check_legal_threat(body: str) -> bool:
        """Check for legal language in email"""
        body_lower = body.lower()
        return any(keyword in body_lower for keyword in LEGAL_KEYWORDS)
    
    @staticmethod
    def check_refund_demand(body: str) -> bool:
        """Check for explicit refund demands"""
        body_lower = body.lower()
        return any(keyword in body_lower for keyword in REFUND_KEYWORDS)
    
    @staticmethod
    def check_angry_tone(sentiment: str) -> bool:
        """Check if sentiment is very negative"""
        return sentiment == "Negative"
    
    @staticmethod
    def check_repeated_contact(contact_count: int = 1) -> bool:
        """Check if customer has contacted multiple times"""
        threshold = ESCALATION_THRESHOLDS.get("repeated_contact_count", 2)
        return contact_count >= threshold
    
    @staticmethod
    def check_high_urgency(urgency: str) -> bool:
        """Check if urgency is High"""
        return urgency == "High"
    
    @staticmethod
    def check_medium_urgency(urgency: str) -> bool:
        """Check if urgency is Medium"""
        return urgency == "Medium"
    
    @staticmethod
    def evaluate(classification: dict, email_body: str, contact_count: int = 1) -> tuple[bool, str]:
        """
        Master escalation evaluator - IMPROVED with confidence thresholds
        
        Args:
            classification: Dict with category, urgency, sentiment, confidence
            email_body: Raw email text
            contact_count: Number of times customer contacted (default 1)
        
        Returns:
            (escalate: bool, reason: str)
        """
        
        if not classification:
            return True, "No classification provided"
        
        urgency = classification.get("urgency", "Low")
        sentiment = classification.get("sentiment", "Neutral")
        confidence = classification.get("confidence", 0.0)
        
        # ===== RULE 1: Legal threat detected - ALWAYS ESCALATE =====
        if EscalationRules.check_legal_threat(email_body):
            return True, "Legal threat detected"
        
        # ===== RULE 2: Explicit refund demand - ALWAYS ESCALATE =====
        if EscalationRules.check_refund_demand(email_body):
            return True, "Refund demand detected"
        
        # ===== RULE 3: High urgency + Negative sentiment (ONLY if high confidence) =====
        # IMPROVED: Only escalate if we're very confident it's angry
        if EscalationRules.check_high_urgency(urgency) and EscalationRules.check_angry_tone(sentiment):
            if confidence >= 0.90:  # Only escalate if 90%+ confident
                return True, f"High urgency + Negative sentiment (confidence: {confidence:.2f})"
            else:
                # Low confidence = give benefit of doubt
                return False, None
        
        # ===== RULE 4: Medium urgency + Negative sentiment = AUTO-DRAFT =====
        # IMPROVED: Frustrated but not critical = still auto-draft
        if EscalationRules.check_medium_urgency(urgency) and EscalationRules.check_angry_tone(sentiment):
            # Even if negative sentiment, if urgency is only Medium = auto-draft
            return False, None
        
        # ===== RULE 5: Repeated contact (2+) with High urgency + Negative =====
        # IMPROVED: Only escalate if very confident
        if EscalationRules.check_repeated_contact(contact_count):
            if EscalationRules.check_high_urgency(urgency) and EscalationRules.check_angry_tone(sentiment):
                if confidence >= 0.85:  # 85% confident
                    return True, f"Repeated contact ({contact_count}) + High urgency + Negative (confidence: {confidence:.2f})"
                else:
                    return False, None
            elif EscalationRules.check_medium_urgency(urgency) and EscalationRules.check_angry_tone(sentiment):
                # Repeated contact with Medium urgency = still auto-draft
                return False, None
        
        # ===== RULE 6: Low confidence in classification =====
        # IMPROVED: If we're unsure about classification, auto-draft instead of escalating
        if confidence < 0.75:
            return False, None  # Give benefit of doubt
        
        # ===== DEFAULT: No escalation needed =====
        return False, None
    
    @staticmethod
    def get_escalation_priority(classification: dict, email_body: str, contact_count: int = 1) -> str:
        """
        Determine priority level for escalation
        
        Returns: "Critical", "High", "Medium", "Low", "None"
        """
        
        escalate, reason = EscalationRules.evaluate(classification, email_body, contact_count)
        
        if not escalate:
            return "None"
        
        urgency = classification.get("urgency", "Low")
        sentiment = classification.get("sentiment", "Neutral")
        
        # Critical: Legal or refund demand
        if EscalationRules.check_legal_threat(email_body):
            return "Critical"
        if EscalationRules.check_refund_demand(email_body):
            return "Critical"
        
        # High: High urgency + Negative (with high confidence)
        if urgency == "High" and sentiment == "Negative":
            return "High"
        
        # Medium: Repeated contact with issues
        if contact_count >= 2:
            return "Medium"
        
        # Low: Other escalations
        return "Low"
    
    @staticmethod
    def format_escalation_summary(classification: dict, email_body: str, contact_count: int = 1) -> dict:
        """Format complete escalation decision with reasoning"""
        
        escalate, reason = EscalationRules.evaluate(classification, email_body, contact_count)
        priority = EscalationRules.get_escalation_priority(classification, email_body, contact_count)
        
        return {
            "should_escalate": escalate,
            "reason": reason,
            "priority": priority,
            "details": {
                "urgency": classification.get("urgency"),
                "sentiment": classification.get("sentiment"),
                "confidence": classification.get("confidence"),
                "contact_count": contact_count,
                "has_legal_threat": EscalationRules.check_legal_threat(email_body),
                "has_refund_demand": EscalationRules.check_refund_demand(email_body),
            }
        }