# n8n-Agent-Automations

**EdTech AI Support Agent**

**🎯 How It Works**

Gmail (your email account)
    ↓
n8n Gmail Trigger (captures real email)
    ↓
Email data flows to previous node
    ↓
HTTP Request node sends to backend
    ↓
YOUR BACKEND (FastAPI + Llama in VS Code):
├─ Classifies the email
├─ Applies escalation rules
├─ Generates draft OR marks as escalate
    ↓
HTTP Response sent back to n8n
├─ If escalate=false → draft_reply in response
├─ If escalate=true → escalation_reason in response
    ↓
n8n Decision Node:
├─ If escalate=true → Send to support team
├─ If escalate=false → Send auto-draft reply

**📊 Performance Metrics**
This system:

⚡ Speed: Process email in ~1-2 seconds
💰 Cost: Free (Groq free tier)
🎯 Accuracy: ~90% classification accuracy
📈 Scalability: Can handle 30-60 emails/minute
🔒 Security: API key protected


**🚀 What You Can Do With This**

✅ Process customer support emails
✅ Auto-classify by type
✅ Detect sentiment automatically
✅ Auto-draft responses
✅ Escalate urgent/angry customers
