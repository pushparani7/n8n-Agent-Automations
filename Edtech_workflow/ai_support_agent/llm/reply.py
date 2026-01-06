
# Automated Reply Generation Engine

class ReplyGenerator:
    """Generates automated replies for support emails"""
    
    def __init__(self):
        """Initialize the reply generator"""
        self.templates = self._load_templates()
        print("✅ ReplyGenerator initialized")
    
    def _load_templates(self) -> dict:
        """Load reply templates for different categories"""
        return {
            "Technical Issues": {
                "Platform Access": "Thank you for reaching out! We're sorry you're experiencing access issues. Our technical team is looking into this. Please try clearing your browser cache and logging in again. If the issue persists, please reply with your account details and we'll investigate immediately.",
                "Video Playback": "Thank you for reporting the video playback issue. This is often due to browser compatibility or internet speed. Please try: 1) Using a different browser, 2) Clearing your cache, or 3) Checking your internet connection. Let us know if the issue continues!",
                "Course Materials": "We appreciate you contacting us about the course materials. You should be able to access all materials from the course dashboard. If you're unable to download or view materials, please verify your course enrollment status. Contact us with your course name and we'll help!",
                "Account Login": "Thank you for reaching out about login issues. Please try resetting your password using the 'Forgot Password' link on the login page. If you still can't access your account, we're here to help - please provide your registered email and account details.",
                "Browser Compatibility": "Great question! Our platform works best on Chrome, Firefox, Safari, and Edge (latest versions). If you're using an older browser, please update it or try a different browser. Let us know if this resolves your issue!"
            },
            "Payment & Billing": {
                "Refund Request": "Thank you for contacting us about a refund. We have a 30-day money-back guarantee on all courses. Please reply with your order ID and reason for the refund, and we'll process it within 5-7 business days.",
                "Payment Failed": "Sorry to hear your payment didn't go through! This can happen due to various reasons. Please try: 1) Using a different payment method, 2) Checking with your bank, or 3) Contacting us with your order details and we'll help troubleshoot.",
                "Invoice": "Thank you for requesting an invoice. Invoices are automatically sent to your registered email after purchase. You can also download invoices from your account dashboard under 'Billing History'. Let us know if you need any assistance!",
                "Subscription": "Thank you for your question about subscriptions. You can manage your subscription (renew or cancel) from your account settings. If you need help, please contact us with your subscription details and we'll assist you promptly.",
                "Course Pricing": "We appreciate your interest in our courses! Our pricing reflects the quality content and instructor expertise. We regularly offer discounts and promotions - check your email or visit our pricing page for current offers!"
            },
            "Course Content": {
                "Course Completion": "Great job working through the course! Once you've completed all modules, you'll be able to access your certificate. If you've completed everything and don't see the option, please let us know the course name and we'll verify your completion status.",
                "Certificate": "Congratulations on completing the course! Your certificate is available in your dashboard under 'My Certificates'. You can download it as a PDF or share it directly. If you don't see it, please ensure you've completed all required modules.",
                "Curriculum": "Thank you for your question about the course curriculum. You can view the detailed curriculum on the course page before enrolling. If you need more information about specific topics or modules, feel free to ask and we'll provide more details!",
                "Course Duration": "The course duration varies by course and your learning pace. Most courses can be completed in 4-8 weeks with 5-10 hours per week. You'll have lifetime access to the materials, so you can learn at your own speed. Let us know if you need more details!",
                "Content Quality": "We're committed to providing high-quality educational content. Each course is created by industry experts and regularly updated. If you have specific feedback or suggestions, we'd love to hear it! Please share your thoughts and we'll take them into consideration."
            },
            "Account Management": {
                "Profile Update": "You can update your profile information by going to Account Settings. Simply click on your profile picture in the top-right corner and select 'Account Settings'. If you need help with any specific field, let us know!",
                "Password Reset": "To reset your password, click 'Forgot Password' on the login page. You'll receive an email with reset instructions. If you don't see the email, please check your spam folder or contact us for assistance.",
                "Account Deletion": "We're sorry to see you go! To delete your account, please contact our support team with your request. Note that this action is irreversible and you'll lose access to all courses. We'd love to hear feedback on why you're leaving!",
                "Email Change": "To change your email, go to Account Settings and update your email address. You'll receive a confirmation email at your new address. If you encounter any issues, please contact us and we'll help you change it securely.",
                "Two Factor Auth": "For added security, you can enable two-factor authentication in your Account Settings. This adds an extra layer of protection to your account. Once enabled, you'll need to provide a code from your authenticator app when logging in."
            },
            "General Queries": {
                "default": "Thank you for reaching out to us! We appreciate your inquiry. Our team will review your message and get back to you within 24 hours. In the meantime, if you have any urgent questions, please let us know!"
            }
        }
    
    def generate_with_fallback(self, subject: str, body: str, category: str, sentiment: str) -> tuple:
        """
        Generate a reply with fallback options
        
        Args:
            subject (str): Email subject
            body (str): Email body
            category (str): Email category
            sentiment (str): Email sentiment
            
        Returns:
            tuple: (reply_text, source)
        """
        # Try to get template-based reply
        reply = self._get_template_reply(category)
        
        if reply:
            return reply, "template"
        
        # Fallback to generic reply
        return self._get_generic_reply(sentiment), "fallback"
    
    def _get_template_reply(self, category: str) -> str:
        """Get reply from template"""
        if category not in self.templates:
            return None
        
        # Get the template for this category
        category_templates = self.templates[category]
        
        # If there's a default, return it (for single-item categories)
        if "default" in category_templates:
            return category_templates["default"]
        
        # Otherwise return the first available template
        if category_templates:
            return next(iter(category_templates.values()))
        
        return None
    
    def _get_generic_reply(self, sentiment: str) -> str:
        """Get generic reply based on sentiment"""
        if sentiment == "Negative":
            return "Thank you for reaching out. We sincerely apologize for any inconvenience you've experienced. Our team is committed to resolving this issue as quickly as possible. Please provide us with more details and we'll prioritize your case."
        elif sentiment == "Positive":
            return "Thank you so much for your kind message! We're thrilled that you're having a great experience. If you have any questions or need assistance, please don't hesitate to reach out!"
        else:
            return "Thank you for contacting us. We appreciate your inquiry and will get back to you shortly with a helpful response. Please let us know if there's anything else we can assist you with."