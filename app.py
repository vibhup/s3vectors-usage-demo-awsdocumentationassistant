#!/usr/bin/env python3
"""
AWS Documentation RAG System - Web Application

A Flask-based web interface for the AWS Documentation RAG System that allows users
to ask questions about AWS services and get comprehensive answers powered by
Claude 3.5 Sonnet and S3 Vectors.

Features:
- Modern, responsive web interface
- Real-time question processing
- Structured answer display with sources
- Chat history and conversation memory
- Mobile-friendly design
- Error handling and loading states

Usage:
    python3 app.py
    Then open http://localhost:5000 in your browser
"""

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import json
import boto3
import logging
from typing import List, Dict, Any
from datetime import datetime
import uuid
import os

# Import our RAG system
from aws_docs_rag_system import AWSDocsRAGSystem

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management
CORS(app)  # Enable CORS for API calls

# Global RAG system instance
rag_system = None

def initialize_rag_system():
    """Initialize the RAG system with proper configuration."""
    global rag_system
    try:
        rag_system = AWSDocsRAGSystem(
            vector_bucket_name="vibhup-aws-docs-vectors",
            index_name="aws-documentation",
            s3vectors_region="us-east-1",
            bedrock_region="us-east-1"
        )
        logger.info("RAG System initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize RAG system: {str(e)}")
        return False

@app.route('/')
def index():
    """Main page route."""
    # Initialize session if needed
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
        session['chat_history'] = []
    
    return render_template('index.html')

@app.route('/api/ask', methods=['POST'])
def ask_question():
    """API endpoint to process user questions."""
    try:
        data = request.get_json()
        user_question = data.get('question', '').strip()
        
        if not user_question:
            return jsonify({
                'success': False,
                'error': 'Please provide a question'
            }), 400
        
        # Check if RAG system is initialized
        if not rag_system:
            return jsonify({
                'success': False,
                'error': 'RAG system not initialized. Please check AWS credentials and try again.'
            }), 500
        
        # Process the question
        logger.info(f"Processing question: {user_question}")
        result = rag_system.process_question(user_question, top_k=5)
        
        # Add to chat history
        if 'chat_history' not in session:
            session['chat_history'] = []
        
        chat_entry = {
            'id': str(uuid.uuid4()),
            'question': user_question,
            'answer': result['answer'],
            'sources': result['sources'],
            'timestamp': result['timestamp'],
            'model_used': result['model_used'],
            'documents_retrieved': result['documents_retrieved']
        }
        
        session['chat_history'].append(chat_entry)
        session.modified = True
        
        return jsonify({
            'success': True,
            'data': chat_entry
        })
        
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'An error occurred while processing your question: {str(e)}'
        }), 500

@app.route('/api/history')
def get_chat_history():
    """Get chat history for the current session."""
    try:
        history = session.get('chat_history', [])
        return jsonify({
            'success': True,
            'data': history
        })
    except Exception as e:
        logger.error(f"Error getting chat history: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/clear-history', methods=['POST'])
def clear_chat_history():
    """Clear chat history for the current session."""
    try:
        session['chat_history'] = []
        session.modified = True
        return jsonify({
            'success': True,
            'message': 'Chat history cleared'
        })
    except Exception as e:
        logger.error(f"Error clearing chat history: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint."""
    try:
        # Check if RAG system is working
        system_status = {
            'rag_system_initialized': rag_system is not None,
            'timestamp': datetime.now().isoformat(),
            'status': 'healthy' if rag_system else 'degraded'
        }
        
        return jsonify({
            'success': True,
            'data': system_status
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/examples')
def get_example_questions():
    """Get example questions for users."""
    examples = [
        {
            'category': 'Compute & Serverless',
            'questions': [
                'How do I scale Lambda functions automatically?',
                'What are the best practices for Lambda memory optimization?',
                'When should I use EC2 vs Lambda for my workload?',
                'How to implement auto-scaling for EC2 instances?'
            ]
        },
        {
            'category': 'Storage & Databases',
            'questions': [
                'What are the best security practices for S3 buckets?',
                'How to optimize DynamoDB read and write performance?',
                'What are the different S3 storage classes and when to use them?',
                'How to implement RDS backup and recovery strategies?'
            ]
        },
        {
            'category': 'Networking & Security',
            'questions': [
                'How to configure VPC security groups vs NACLs?',
                'What are IAM policy best practices?',
                'How to implement AWS security monitoring?',
                'What are the Route 53 DNS routing policies?'
            ]
        },
        {
            'category': 'Architecture & Best Practices',
            'questions': [
                'What are the AWS Well-Architected Framework principles?',
                'How to implement cost optimization strategies?',
                'What are the best practices for multi-region deployments?',
                'How to design fault-tolerant AWS architectures?'
            ]
        }
    ]
    
    return jsonify({
        'success': True,
        'data': examples
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return render_template('500.html'), 500

if __name__ == '__main__':
    print("🚀 Starting AWS Documentation RAG System Web Application")
    print("=" * 60)
    
    # Initialize RAG system
    print("📡 Initializing RAG System...")
    if initialize_rag_system():
        print("✅ RAG System initialized successfully")
        print("🌐 Starting web server...")
        print("📱 Open http://localhost:5000 in your browser")
        print("=" * 60)
        
        # Run Flask app
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            threaded=True
        )
    else:
        print("❌ Failed to initialize RAG system")
        print("💡 Please check your AWS credentials and try again")
        print("=" * 60)
