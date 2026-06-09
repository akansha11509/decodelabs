"""
Flask REST API Server for Advanced Rule-Based Chatbot
Provides endpoints for chat interactions with unique features
"""

from flask import Flask, request, jsonify
from chatbot import chat, AdvancedRuleBasedChatbot
from flask_cors import CORS
from datetime import datetime
from pytz import timezone
import uuid
import os

app = Flask(__name__)

# Enable CORS for cross-domain requests
CORS(app)

# Initialize chatbot with advanced features
chatbot_instance = AdvancedRuleBasedChatbot(bot_name="Assistant")

# Session key for security
app.secret_key = os.urandom(24)


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error=None):
    """Handle 404 Not Found errors."""
    return jsonify({
        'status': 404,
        'message': f'Not Found: {request.url}',
    }), 404


@app.errorhandler(500)
def internal_server_error(error=None):
    """Handle 500 Internal Server Error."""
    return jsonify({
        'status': 500,
        'message': 'Unexpected server error or Internal Server Error',
    }), 500


@app.errorhandler(400)
def bad_request(error=None):
    """Handle 400 Bad Request."""
    return jsonify({
        'status': 400,
        'message': 'Bad request - invalid parameters',
    }), 400


# ==================== ROUTES ====================

@app.route('/', methods=['GET'])
def home():
    """Home endpoint showing API information."""
    return jsonify({
        'status': 200,
        'message': 'Advanced Rule-Based AI Chatbot API',
        'version': '1.0',
        'endpoints': {
            'POST /api/chat': 'Send a message and get response',
            'GET /api/history/<user_id>': 'Get conversation history',
            'POST /api/session/new': 'Create new conversation session',
            'GET /api/analytics/<user_id>': 'Get conversation analytics',
            'GET /api/capabilities': 'Get chatbot features',
            'GET /api/health': 'Health check',
        }
    }), 200


@app.route('/api/chat', methods=['POST'])
def chat_endpoint():
    """
    Main chat endpoint with advanced features.
    
    Request:
    {
        "user_id": "string",
        "message": "string"
    }
    
    Response includes: intent, sentiment, entities, confidence, etc.
    """
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                'status': 400,
                'error': 'Missing required field: message',
            }), 400
        
        user_message = data.get('message', '').strip()
        user_id = data.get('user_id', str(uuid.uuid4()))
        
        if not user_message:
            return jsonify({
                'status': 400,
                'error': 'Message cannot be empty',
            }), 400
        
        # Get response from chatbot
        response = chatbot_instance.get_response(user_message, user_id)
        response['status'] = 200
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({
            'status': 500,
            'error': f'Error processing request: {str(e)}',
        }), 500


@app.route('/api/history/<user_id>', methods=['GET'])
def get_history(user_id):
    """Get conversation history for a user."""
    try:
        history = chatbot_instance.get_conversation_history(user_id)
        
        return jsonify({
            'status': 200,
            'user_id': user_id,
            'total_messages': len(history),
            'history': history,
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 500,
            'error': f'Error retrieving history: {str(e)}',
        }), 500


@app.route('/api/session/new', methods=['POST'])
def create_session():
    """Create a new conversation session."""
    try:
        user_id = str(uuid.uuid4())
        timestamp = datetime.now(timezone('Asia/Kolkata')).isoformat()
        
        return jsonify({
            'status': 201,
            'user_id': user_id,
            'session_created': timestamp,
            'message': 'New session created successfully'
        }), 201
        
    except Exception as e:
        return jsonify({
            'status': 500,
            'error': f'Error creating session: {str(e)}',
        }), 500


@app.route('/api/analytics/<user_id>', methods=['GET'])
def get_analytics(user_id):
    """Get conversation analytics for a user."""
    try:
        analytics = chatbot_instance.get_analytics(user_id)
        analytics['status'] = 200
        
        return jsonify(analytics), 200
        
    except Exception as e:
        return jsonify({
            'status': 500,
            'error': f'Error retrieving analytics: {str(e)}',
        }), 500


@app.route('/api/capabilities', methods=['GET'])
def get_capabilities():
    """Get chatbot capabilities and unique features."""
    try:
        return jsonify({
            'status': 200,
            'bot_name': chatbot_instance.bot_name,
            'unique_features': [
                'Context Memory - Remembers previous conversation turns',
                'Sentiment Analysis - Detects positive, negative, neutral',
                'Entity Extraction - Finds emails, phones, URLs, numbers',
                'Conversation Learning - Tracks and learns from queries',
                'Analytics - Provides conversation insights',
                'Smart Fallbacks - Intelligent default responses',
            ],
            'supported_intents': list(chatbot_instance.rules.keys()),
            'entity_types': list(chatbot_instance.entity_patterns.keys()),
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 500,
            'error': f'Error retrieving capabilities: {str(e)}',
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 200,
        'health': 'OK',
        'bot_name': chatbot_instance.bot_name,
        'timestamp': datetime.now(timezone('UTC')).isoformat(),
    }), 200




if __name__ == '__main__':
    print("🚀 Starting Advanced Rule-Based AI Chatbot Server...")
    print("📍 Server running on: http://127.0.0.1:5000")
    print("💡 Key Endpoints:")
    print("   POST /api/chat - Send a message")
    print("   GET  /api/history/<user_id> - Get conversation history")
    print("   POST /api/session/new - Create new session")
    print("   GET  /api/analytics/<user_id> - Get analytics")
    print("   GET  /api/capabilities - Get chatbot features")
    print("   GET  /api/health - Health check")
    print("\n✨ Press CTRL+C to stop the server\n")
    
    app.run(debug=True, host='127.0.0.1', port=5000)