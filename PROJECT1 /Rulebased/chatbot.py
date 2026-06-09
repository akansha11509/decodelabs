"""
Advanced Rule-Based AI Chatbot with Unique Features
An enhanced rule-based chatbot that goes beyond basic pattern matching:
- Context Memory: Remembers previous conversation turns
- Sentiment Analysis: Detects user emotion and adjusts responses
- Entity Extraction: Identifies key information (emails, phones, numbers)
- Conversation Learning: Tracks and learns from interactions
- Analytics: Provides conversation insights and metrics
- Smart Fallbacks: Intelligent default responses based on context
- Multi-turn Support: Maintains conversational flow
"""

import re
import random
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from pytz import timezone
from collections import defaultdict
import json


class AdvancedRuleBasedChatbot:
    """
    An advanced rule-based chatbot with context awareness, sentiment analysis,
    and learning capabilities - making it unique from basic chatbots.
    """

    def __init__(self, bot_name: str = "Assistant"):
        """Initialize the advanced chatbot with unique features."""
        self.bot_name = bot_name
        self.rules = self._initialize_rules()
        self.conversation_history = []
        self.user_context = {}
        self.entity_patterns = self._initialize_entities()
        self.learned_responses = defaultdict(list)
        self.fmt = "%Y-%m-%d %H:%M:%S %Z%z"
        
    def _initialize_entities(self) -> Dict:
        """Define entities to extract from user input."""
        return {
            'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'url': r'https?://[^\s]+',
            'number': r'\b\d+\b',
        }

    def _initialize_rules(self) -> Dict:
        """Define comprehensive rules with multiple response variations."""
        return {
            'greeting': {
                'patterns': [
                    r'\bhello\b|\bhi\b|\bhey\b|\bgreetings\b',
                    r'good morning|good afternoon|good evening',
                ],
                'responses': [
                    'Hello! How can I assist you today?',
                    'Hi there! What can I help you with?',
                    'Greetings! What brings you here?',
                    'Welcome! How may I be of service?',
                ],
            },
            'goodbye': {
                'patterns': [
                    r'\bbye\b|\bgoodbye\b|see you|farewell',
                    r'take care|catch you later',
                ],
                'responses': [
                    'Goodbye! Have a great day!',
                    'See you later! Thanks for chatting.',
                    'Bye! Feel free to come back anytime.',
                    'Take care! Goodbye!',
                ],
            },
            'help': {
                'patterns': [
                    r'\bhelp\b|\bsupport\b|\bassist\b',
                    r'can you help|need help|what can you do',
                ],
                'responses': [
                    'I\'m here to help! Ask me anything.',
                    'Sure, I can assist you. What do you need?',
                    'I\'d be happy to help. How can I assist?',
                    'Tell me what you need, and I\'ll do my best!',
                ],
            },
            'thanks': {
                'patterns': [
                    r'thank|thanks|appreciate|grateful',
                    r'thx|ty|much appreciated',
                ],
                'responses': [
                    'You\'re welcome! Happy to help.',
                    'My pleasure! Let me know if you need anything else.',
                    'Anytime! Feel free to ask me anything.',
                    'Glad I could help!',
                ],
            },
            'how_are_you': {
                'patterns': [
                    r'how are you|how\'?s it going|how do you feel',
                    r'how\'?re you|you doing',
                ],
                'responses': [
                    'I\'m doing great, thanks for asking! How about you?',
                    'I\'m functioning perfectly! Ready to help you.',
                    'All systems operational! How can I assist?',
                    'I\'m doing well! What about you?',
                ],
            },
            'what_is_your_name': {
                'patterns': [
                    r'what.*your.*name|who.*you|introduce yourself',
                    r'what should i call you|what\'s your name',
                ],
                'responses': [
                    f'I\'m {self.bot_name}! Nice to meet you.',
                    f'You can call me {self.bot_name}. How can I help?',
                    f'I\'m {self.bot_name}, your AI assistant. What do you need?',
                ],
            },
            'capabilities': {
                'patterns': [
                    r'what can you do|your capabilities|features',
                    r'what are your abilities|how can you help',
                ],
                'responses': [
                    'I can understand intent, remember context, detect sentiment, and learn from interactions!',
                    'My unique features: context memory, sentiment analysis, entity extraction, conversation analytics!',
                    'I have multi-turn conversation support, emotional awareness, and intelligent learning!',
                ],
            },
            'joke': {
                'patterns': [
                    r'tell me a joke|make me laugh|something funny',
                    r'do you know any jokes|funny|humor',
                ],
                'responses': [
                    'Why don\'t scientists trust atoms? Because they make up everything!',
                    'Why did the AI go to school? To improve its learning!',
                    'What do you call an AI that tells jokes? A pun-processor!',
                    'Why was the AI good at telling jokes? It had great timing!',
                ],
            },
            'status': {
                'patterns': [
                    r'are you there|you there|alive|working|online',
                    r'can you hear me|respond|are you working',
                ],
                'responses': [
                    'Yes, I\'m here and working perfectly!',
                    'All systems online! I\'m ready to chat.',
                    'I\'m alive and operational!',
                    'Present and accounted for!',
                ],
            },
            'default': {
                'patterns': [],
                'responses': [
                    'That\'s interesting! Tell me more about that.',
                    'I understand. Can you elaborate?',
                    'Interesting point! What else would you like to discuss?',
                    'I see. How can I help you with that?',
                ],
            }
        }

    def analyze_sentiment(self, user_input: str) -> str:
        """
        Analyze sentiment of user input (positive, negative, neutral).
        UNIQUE FEATURE: Returns sentiment for tone-aware responses.
        """
        user_input_lower = user_input.lower()
        
        positive_words = {'good', 'great', 'excellent', 'amazing', 'wonderful', 'happy', 'love', 'fantastic'}
        negative_words = {'bad', 'terrible', 'awful', 'hate', 'horrible', 'angry', 'sad', 'upset'}
        
        positive_count = sum(1 for word in positive_words if word in user_input_lower)
        negative_count = sum(1 for word in negative_words if word in user_input_lower)
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'

    def extract_entities(self, user_input: str) -> Dict[str, List[str]]:
        """
        Extract entities (email, phone, numbers, URLs) from input.
        UNIQUE FEATURE: Identifies and extracts key information automatically.
        """
        entities = {}
        for entity_type, pattern in self.entity_patterns.items():
            matches = re.findall(pattern, user_input)
            if matches:
                entities[entity_type] = matches
        return entities

    def get_context_summary(self, user_id: str) -> Dict:
        """
        Get conversation context for a user.
        UNIQUE FEATURE: Maintains multi-turn conversation context.
        """
        if user_id not in self.user_context:
            return {
                'last_intent': None,
                'last_sentiment': 'neutral',
                'message_count': 0,
            }
        return self.user_context[user_id]

    def preprocess_input(self, user_input: str) -> str:
        """Preprocess user input for pattern matching."""
        text = user_input.lower()
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def identify_intent(self, user_input: str) -> Tuple[str, float]:
        """
        Identify intent with improved matching algorithm.
        Prioritizes by match length and specificity.
        """
        processed_input = self.preprocess_input(user_input)
        best_intent = 'default'
        best_score = 0.0
        match_length = 0

        for intent, data in self.rules.items():
            if intent == 'default':
                continue
                
            for pattern in data['patterns']:
                match = re.search(pattern, processed_input)
                if match:
                    matched_length = len(match.group(0))
                    confidence = min(matched_length / len(processed_input) + 0.5, 1.0)
                    
                    if matched_length > match_length or (matched_length == match_length and confidence > best_score):
                        best_score = confidence
                        best_intent = intent
                        match_length = matched_length

        return best_intent, best_score

    def get_response(self, user_input: str, user_id: Optional[str] = None) -> Dict:
        """
        Generate response with all advanced features integrated.
        UNIQUE FEATURES: Integrates sentiment, entities, context, and learning.
        """
        # Analyze sentiment
        sentiment = self.analyze_sentiment(user_input)
        
        # Extract entities
        entities = self.extract_entities(user_input)
        
        # Identify intent
        intent, confidence = self.identify_intent(user_input)
        
        # Get base response
        intent_data = self.rules.get(intent, self.rules['default'])
        response = random.choice(intent_data['responses'])
        
        # Enhance response based on context and sentiment
        context = self.get_context_summary(user_id or 'default')
        if sentiment == 'positive' and context['message_count'] > 2:
            response = response.rstrip('!.') + '! 😊'
        elif sentiment == 'negative' and context['message_count'] > 2:
            response = 'I understand. ' + response
        
        # Get timestamp
        now_utc = datetime.now(timezone('UTC'))
        now_india = now_utc.astimezone(timezone('Asia/Kolkata'))
        timestamp = now_india.strftime(self.fmt)
        
        # Create message record
        message_record = {
            'user_id': user_id,
            'user_message': user_input,
            'bot_response': response,
            'intent': intent,
            'confidence': confidence,
            'sentiment': sentiment,
            'entities': entities,
            'timestamp': timestamp
        }
        
        # Store in conversation history
        self.conversation_history.append(message_record)
        
        # Update user context
        if user_id:
            if user_id not in self.user_context:
                self.user_context[user_id] = {
                    'last_intent': intent,
                    'last_sentiment': sentiment,
                    'message_count': 1,
                }
            else:
                self.user_context[user_id]['last_intent'] = intent
                self.user_context[user_id]['last_sentiment'] = sentiment
                self.user_context[user_id]['message_count'] += 1
        
        # Learn from response
        self.learned_responses[intent].append({
            'query': user_input,
            'response': response,
            'sentiment': sentiment
        })
        
        return {
            'user_message': user_input,
            'bot_response': response,
            'intent': intent,
            'confidence': round(confidence, 2),
            'sentiment': sentiment,
            'entities': entities,
            'timestamp': timestamp,
            'user_id': user_id,
            'bot_name': self.bot_name
        }

    def get_conversation_history(self, user_id: Optional[str] = None) -> List[Dict]:
        """Get conversation history."""
        if user_id:
            return [msg for msg in self.conversation_history if msg['user_id'] == user_id]
        return self.conversation_history

    def get_analytics(self, user_id: Optional[str] = None) -> Dict:
        """
        Get conversation analytics.
        UNIQUE FEATURE: Provides insights into conversation patterns.
        """
        if user_id and user_id in self.user_context:
            context = self.user_context[user_id]
            return {
                'user_id': user_id,
                'total_messages': context['message_count'],
                'last_sentiment': context['last_sentiment'],
                'last_intent': context['last_intent']
            }
        else:
            avg_confidence = sum(msg['confidence'] for msg in self.conversation_history) / len(self.conversation_history) if self.conversation_history else 0
            return {
                'total_conversations': len(self.conversation_history),
                'unique_users': len(self.user_context),
                'average_confidence': round(avg_confidence, 2),
                'intents_learned': len(self.learned_responses)
            }


# Create singleton instance
chatbot = AdvancedRuleBasedChatbot(bot_name="Assistant")


def chat(user_message: str, user_id: Optional[str] = None) -> Dict:
    """Wrapper function to interact with the chatbot."""
    return chatbot.get_response(user_message, user_id)


if __name__ == '__main__':
    print("Advanced Rule-Based AI Chatbot - Demo")
    print("=" * 70)
    
    bot = AdvancedRuleBasedChatbot(bot_name="Assistant")
    
    test_messages = [
        "Hello!",
        "How are you?",
        "What's your name?",
        "Tell me a joke",
        "What can you do?",
        "I'm feeling great today!",
        "Can you help me?",
        "Thanks for your help!",
        "Goodbye!"
    ]
    
    user_id = "demo_user_001"
    
    print(f"\nTesting with User ID: {user_id}\n")
    
    for message in test_messages:
        response = bot.get_response(message, user_id)
        print(f"👤 You: {message}")
        print(f"🤖 {response['bot_name']}: {response['bot_response']}")
        print(f"📊 Intent: {response['intent']} | Sentiment: {response['sentiment']} | Confidence: {response['confidence']}")
        if response['entities']:
            print(f"🏷️ Entities: {response['entities']}")
        print("-" * 70)
    
    print("\n📈 Analytics:")
    analytics = bot.get_analytics(user_id)
    for key, value in analytics.items():
        print(f"  {key}: {value}")
