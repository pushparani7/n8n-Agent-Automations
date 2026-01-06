# app.py
# FastAPI Backend Server for EdTech Support Agent

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Import custom modules
from llm.classify import EmailClassifier
from llm.reply import ReplyGenerator
from rules.escalation import EscalationRules
from config.settings import SUPPORT_CATEGORIES

# ============= INITIALIZE COMPONENTS IMMEDIATELY =============
print("\n" + "=" * 70)
print("🚀 Initializing EdTech AI Support Agent API")
print("=" * 70)

print("\n🔄 Loading components...")
try:
    classifier = EmailClassifier()
    reply_generator = ReplyGenerator()
    print("✅ All components loaded successfully!\n")
except Exception as e:
    print(f"\n❌ FAILED TO LOAD COMPONENTS:")
    print(f"   Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ============= PYDANTIC MODELS =============

class EmailInput(BaseModel):
    """Input model for email processing"""
    email_id: str
    subject: str
    body: str
    contact_count: int = 1

class ClassificationResponse(BaseModel):
    """Classification response model"""
    email_id: str
    category: str
    sub_category: str
    urgency: str
    sentiment: str
    confidence: float
    escalate_to_human: bool

class TicketResponse(BaseModel):
    """Complete ticket response model"""
    email_id: str
    subject: str
    category: str
    sub_category: str
    urgency: str
    sentiment: str
    confidence: float
    status: str
    escalate: bool
    escalation_reason: Optional[str]
    escalation_priority: Optional[str]
    draft_reply: Optional[str]
    processed_at: str

class BatchProcessRequest(BaseModel):
    """Batch processing request"""
    emails: List[EmailInput]

class SummaryReport(BaseModel):
    """Summary report model"""
    total_tickets: int
    auto_drafted: int
    escalated: int
    escalation_rate: str
    urgency_breakdown: dict
    sentiment_breakdown: dict
    category_breakdown: dict

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    message: str
    timestamp: str

# ============= FASTAPI APP SETUP =============

app = FastAPI(
    title="🤖 EdTech AI Support Agent",
    description="Automated customer support system",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============= ENDPOINTS =============

@app.get("/", tags=["Info"])
async def root():
    """Root endpoint"""
    return {
        "message": "🤖 EdTech AI Support Agent API",
        "documentation": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        message="EdTech Support Agent is running",
        timestamp=datetime.now().isoformat()
    )

@app.post("/classify", response_model=ClassificationResponse, tags=["Classification"])
async def classify_email(email: EmailInput):
    """Classify a single email"""
    try:
        classification = classifier.classify(email.subject, email.body)
        
        return ClassificationResponse(
            email_id=email.email_id,
            category=classification.get("category", "General Queries"),
            sub_category=classification.get("sub_category", "Unknown"),
            urgency=classification.get("urgency", "Low"),
            sentiment=classification.get("sentiment", "Neutral"),
            confidence=classification.get("confidence", 0.0),
            escalate_to_human=classification.get("escalate_to_human", False)
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Classification error: {str(e)}")

@app.post("/process-ticket", response_model=TicketResponse, tags=["Processing"])
async def process_ticket(email: EmailInput):
    """Process a complete ticket"""
    try:
        # Classify
        classification = classifier.classify(email.subject, email.body)
        
        category = classification.get("category", "General Queries")
        urgency = classification.get("urgency", "Low")
        sentiment = classification.get("sentiment", "Neutral")
        confidence = classification.get("confidence", 0.0)
        
        # Evaluate escalation
        escalation_summary = EscalationRules.format_escalation_summary(
            classification,
            email.body,
            email.contact_count
        )
        
        escalate = escalation_summary.get("should_escalate", False)
        escalation_reason = escalation_summary.get("reason")
        escalation_priority = escalation_summary.get("priority")
        
        # Generate reply (if not escalating)
        draft_reply = None
        if not escalate:
            reply, source = reply_generator.generate_with_fallback(
                email.subject,
                email.body,
                category,
                sentiment
            )
            draft_reply = reply
        
        status = "Escalated to Human" if escalate else "Auto-Drafted"
        
        return TicketResponse(
            email_id=email.email_id,
            subject=email.subject,
            category=category,
            sub_category=classification.get("sub_category", "Unknown"),
            urgency=urgency,
            sentiment=sentiment,
            confidence=confidence,
            status=status,
            escalate=escalate,
            escalation_reason=escalation_reason,
            escalation_priority=escalation_priority,
            draft_reply=draft_reply,
            processed_at=datetime.now().isoformat()
        )
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Processing error: {str(e)}")

@app.post("/webhook/process-email", response_model=TicketResponse, tags=["Webhooks"])
async def webhook_process_email(email: EmailInput):
    """Webhook endpoint for n8n integration"""
    try:
        # Classify
        classification = classifier.classify(email.subject, email.body)
        
        category = classification.get("category", "General Queries")
        urgency = classification.get("urgency", "Low")
        sentiment = classification.get("sentiment", "Neutral")
        confidence = classification.get("confidence", 0.0)
        
        # Evaluate escalation
        escalation_summary = EscalationRules.format_escalation_summary(
            classification,
            email.body,
            email.contact_count
        )
        
        escalate = escalation_summary.get("should_escalate", False)
        escalation_reason = escalation_summary.get("reason")
        escalation_priority = escalation_summary.get("priority")
        
        # Generate reply (if not escalating)
        draft_reply = None
        if not escalate:
            reply, source = reply_generator.generate_with_fallback(
                email.subject,
                email.body,
                category,
                sentiment
            )
            draft_reply = reply
        
        status = "Escalated to Human" if escalate else "Auto-Drafted"
        
        return TicketResponse(
            email_id=email.email_id,
            subject=email.subject,
            category=category,
            sub_category=classification.get("sub_category", "Unknown"),
            urgency=urgency,
            sentiment=sentiment,
            confidence=confidence,
            status=status,
            escalate=escalate,
            escalation_reason=escalation_reason,
            escalation_priority=escalation_priority,
            draft_reply=draft_reply,
            processed_at=datetime.now().isoformat()
        )
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Processing error: {str(e)}")

@app.post("/batch-process", tags=["Processing"])
async def batch_process(request: BatchProcessRequest):
    """Process multiple tickets at once"""
    try:
        results = []
        
        for email in request.emails:
            try:
                classification = classifier.classify(email.subject, email.body)
                
                category = classification.get("category", "General Queries")
                urgency = classification.get("urgency", "Low")
                sentiment = classification.get("sentiment", "Neutral")
                confidence = classification.get("confidence", 0.0)
                
                escalation_summary = EscalationRules.format_escalation_summary(
                    classification,
                    email.body,
                    email.contact_count
                )
                
                escalate = escalation_summary.get("should_escalate", False)
                escalation_reason = escalation_summary.get("reason")
                escalation_priority = escalation_summary.get("priority")
                
                draft_reply = None
                if not escalate:
                    reply, source = reply_generator.generate_with_fallback(
                        email.subject,
                        email.body,
                        category,
                        sentiment
                    )
                    draft_reply = reply
                
                status = "Escalated to Human" if escalate else "Auto-Drafted"
                
                results.append({
                    "email_id": email.email_id,
                    "subject": email.subject,
                    "category": category,
                    "sub_category": classification.get("sub_category", "Unknown"),
                    "urgency": urgency,
                    "sentiment": sentiment,
                    "confidence": round(confidence, 2),
                    "status": status,
                    "escalate": escalate,
                    "escalation_reason": escalation_reason,
                    "escalation_priority": escalation_priority,
                    "draft_reply": draft_reply,
                    "processed_at": datetime.now().isoformat()
                })
            
            except Exception as e:
                results.append({
                    "email_id": email.email_id,
                    "error": str(e),
                    "status": "Error"
                })
        
        total = len(results)
        escalated = sum(1 for r in results if r.get("escalate", False))
        auto_drafted = total - escalated
        
        urgency_breakdown = {}
        sentiment_breakdown = {}
        category_breakdown = {}
        
        for result in results:
            if "error" not in result:
                urgency = result.get("urgency", "Unknown")
                sentiment = result.get("sentiment", "Unknown")
                category = result.get("category", "Unknown")
                
                urgency_breakdown[urgency] = urgency_breakdown.get(urgency, 0) + 1
                sentiment_breakdown[sentiment] = sentiment_breakdown.get(sentiment, 0) + 1
                category_breakdown[category] = category_breakdown.get(category, 0) + 1
        
        summary = SummaryReport(
            total_tickets=total,
            auto_drafted=auto_drafted,
            escalated=escalated,
            escalation_rate=f"{(escalated/total)*100:.1f}%" if total > 0 else "0%",
            urgency_breakdown=urgency_breakdown,
            sentiment_breakdown=sentiment_breakdown,
            category_breakdown=category_breakdown
        )
        
        return {
            "status": "success",
            "tickets": results,
            "summary": summary
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Batch processing error: {str(e)}")

@app.get("/categories", tags=["Info"])
async def get_categories():
    """Get all support categories"""
    return {
        "categories": SUPPORT_CATEGORIES
    }

# ============= RUN SERVER =============

if __name__ == "__main__":
    import uvicorn
    print("\n" + "=" * 70)
    print("📖 Swagger UI: http://localhost:8000/docs")
    print("📖 ReDoc: http://localhost:8000/redoc")
    print("=" * 70 + "\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )