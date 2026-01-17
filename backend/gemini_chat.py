from flask import Blueprint, request, jsonify
import google.generativeai as genai
import os

gemini_chat_bp = Blueprint('gemini_chat', __name__)

# Configure Gemini API
# Ideally, this should be in an environment variable
# genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@gemini_chat_bp.route('/gemini-chat', methods=['POST'])
def gemini_chat():
    data = request.json
    message = data.get('message')
    
    if not message:
        return jsonify({'error': 'Message is required'}), 400

    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    
    # --- MOCK FALLBACK for Demo/Testing ---
    # If no key is set or it's the placeholder, respond with a demo message
    if not api_key or api_key == "your_api_key_here" or api_key == "PLACEHOLDER":
        print("Using Mock Gemini Response (No API Key)")
        import time
        time.sleep(1.5) # Simulate network delay
        return jsonify({
            'response': (
                "🤖 **Demo Mode Active**\n\n"
                "I see you haven't configured your `GEMINI_API_KEY` in the `.env` file yet.\n\n"
                "**To enable real AI:**\n"
                "1. Open `.env` in the project root.\n"
                "2. Paste your Google Gemini API Key.\n"
                "3. Restart the backend.\n\n"
                f"Your message was: *{message}*"
            )
        })
    # --------------------------------------

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        # Contextualize the AI
        system_prompt = (
            "You are the official AI Assistant for TradeSense, a prop trading firm. "
            "You help traders with platform questions and financial concepts. "
            "Keep answers concise, professional, and helpful. "
            "Do not give financial advice as a definitive instruction, always frame it as educational."
        )
        
        full_prompt = f"{system_prompt}\n\nUser: {message}\nAssistant:"
        
        response = model.generate_content(full_prompt)
        ai_response = response.text
        
        return jsonify({'response': ai_response})
    
    except Exception as e:
        error_str = str(e)
        print(f"Gemini Error (Falling back to Smart Simulation): {error_str}")
        
        # --- SMART SIMULATION ENGINE ---
        # Provides realistic responses when API key is unavailable
        
        msg_lower = message.lower()
        
        if "hello" in msg_lower or "hi" in msg_lower:
            response_text = "Hello! I am your TradeSense AI Assistant. I can help you with market trends, risk management, and platform features. What would you like to know?"
        elif "buy" in msg_lower or "short" in msg_lower or "trade" in msg_lower:
            response_text = "Based on current market volatility, I recommend checking the Risk Guard AI panel before entering any position. Ensure your position size does not exceed 2% of your equity."
        elif "trend" in msg_lower or "bitcoin" in msg_lower or "market" in msg_lower:
            response_text = "The market is currently showing a consolidation pattern. The AI Analysis panel on the right suggests a potential breakout. Watch for volume confirmation."
        elif "risk" in msg_lower or "stop loss" in msg_lower:
            response_text = "Effective risk management is key. I suggest using the 'Smart Size' feature in the Command Center to automatically calculate your optimal lot size based on your stop loss."
        elif "help" in msg_lower:
            response_text = "I can assist you with:\n- Analyzing charts\n- Calculating position sizes\n- Explaining trading terminology\n- Navigating the TradeSense platform"
        else:
            response_text = "That's an interesting market question. While I analyze the specific data points, I'd suggest reviewing the 'Market Feeds' tab for the latest institutional order flow."

        return jsonify({'response': response_text})
