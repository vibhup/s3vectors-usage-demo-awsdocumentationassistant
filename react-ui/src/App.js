import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { tomorrow } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { 
  Send, 
  MessageCircle, 
  BookOpen, 
  Zap, 
  Clock, 
  ExternalLink,
  Lightbulb,
  Trash2,
  Loader
} from 'lucide-react';
import './App.css';

// API Configuration - Real API Gateway URL (us-east-1)
const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://YOUR-API-GATEWAY-ID.execute-api.us-east-1.amazonaws.com/prod';

function App() {
  const [question, setQuestion] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [examples, setExamples] = useState({});
  const [showExamples, setShowExamples] = useState(true);
  const chatEndRef = useRef(null);

  // Scroll to bottom of chat
  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [chatHistory]);

  // Load example questions
  useEffect(() => {
    loadExamples();
  }, []);

  const loadExamples = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/examples`);
      if (response.data.success) {
        setExamples(response.data.data);
      }
    } catch (error) {
      console.error('Error loading examples:', error);
      // Fallback examples if API is not available
      setExamples({
        compute: [
          'How do I scale Lambda functions automatically?',
          'What are the best practices for EC2 instance optimization?',
          'When should I use ECS vs EKS for containerized applications?'
        ],
        storage: [
          'What are S3 security best practices?',
          'How to optimize S3 costs with storage classes?',
          'What\'s the difference between EBS volume types?'
        ],
        database: [
          'How to optimize DynamoDB performance?',
          'What are RDS backup and recovery options?',
          'When to use DynamoDB vs RDS?'
        ]
      });
    }
  };

  const askQuestion = async (questionText = question) => {
    if (!questionText.trim()) return;
    
    setLoading(true);
    setShowExamples(false);
    
    // Add user question to chat immediately
    const userMessage = {
      id: Date.now(),
      type: 'question',
      content: questionText,
      timestamp: new Date().toISOString()
    };
    
    setChatHistory(prev => [...prev, userMessage]);
    setQuestion('');
    
    try {
      const response = await axios.post(`${API_BASE_URL}/ask`, {
        question: questionText
      });
      
      if (response.data.success) {
        const answerMessage = {
          id: Date.now() + 1,
          type: 'answer',
          content: response.data.data.answer,
          sources: response.data.data.sources,
          documentsRetrieved: response.data.data.documents_retrieved,
          modelUsed: response.data.data.model_used,
          timestamp: response.data.data.timestamp,
          technicalDetails: response.data.data.technical_details
        };
        
        setChatHistory(prev => [...prev, answerMessage]);
      } else {
        throw new Error(response.data.error || 'Unknown error occurred');
      }
    } catch (error) {
      console.error('Error asking question:', error);
      
      // Add error message to chat
      const errorMessage = {
        id: Date.now() + 1,
        type: 'error',
        content: `Sorry, I encountered an error: ${error.response?.data?.error || error.message}. Please try again.`,
        timestamp: new Date().toISOString()
      };
      
      setChatHistory(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const clearHistory = () => {
    setChatHistory([]);
    setShowExamples(true);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      askQuestion();
    }
  };

  const ExampleQuestions = () => (
    <div className="examples-section">
      <div className="examples-header">
        <Lightbulb className="icon" />
        <h3>Try asking about:</h3>
      </div>
      
      {examples && Object.keys(examples).length > 0 ? (
        Object.entries(examples).map(([categoryKey, questions], categoryIndex) => (
          <div key={categoryIndex} className="example-category">
            <h4>{categoryKey.charAt(0).toUpperCase() + categoryKey.slice(1)}</h4>
            <div className="example-questions">
              {Array.isArray(questions) && questions.map((exampleQuestion, questionIndex) => (
                <button
                  key={questionIndex}
                  className="example-question"
                  onClick={() => askQuestion(exampleQuestion)}
                  disabled={loading}
                >
                  {exampleQuestion}
                </button>
              ))}
            </div>
          </div>
        ))
      ) : (
        <div className="loading-examples">Loading examples...</div>
      )}
    </div>
  );

  const TechnicalDetailsPanel = ({ technicalDetails }) => {
    const [isExpanded, setIsExpanded] = useState(false);

    if (!technicalDetails) return null;

    const formatDuration = (seconds) => {
      return seconds < 1 ? `${(seconds * 1000).toFixed(0)}ms` : `${seconds.toFixed(2)}s`;
    };

    const getServiceIcon = (service) => {
      const icons = {
        'bedrock-runtime': '🧠',
        's3vectors': '🗄️',
        'lambda': '⚡',
        'apigateway': '🌐'
      };
      return icons[service] || '🔧';
    };

    return (
      <div className="technical-details">
        <button 
          className="technical-toggle"
          onClick={() => setIsExpanded(!isExpanded)}
        >
          <span className="toggle-icon">{isExpanded ? '▼' : '▶'}</span>
          🔧 Technical Details ({formatDuration(technicalDetails.total_duration)})
        </button>
        
        {isExpanded && (
          <div className="technical-content">
            <div className="execution-timeline">
              <h5>⏱️ Execution Timeline</h5>
              <div className="timeline-steps">
                {technicalDetails.steps.map((step, index) => (
                  <div key={index} className="timeline-step">
                    <div className="step-indicator">✅</div>
                    <div className="step-content">
                      <div className="step-name">{step.step.replace(/_/g, ' ').toUpperCase()}</div>
                      <div className="step-description">{step.description}</div>
                      <div className="step-timing">{formatDuration(step.duration_from_start)}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="api-calls">
              <h5>🌐 AWS API Calls</h5>
              <div className="api-list">
                {technicalDetails.api_calls.map((call, index) => (
                  <div key={index} className="api-call">
                    <div className="api-header">
                      <span className="service-icon">{getServiceIcon(call.service)}</span>
                      <span className="api-name">{call.service}:{call.operation}</span>
                      <span className="api-timing">{formatDuration(call.duration_from_start)}</span>
                    </div>
                    {call.details && Object.keys(call.details).length > 0 && (
                      <div className="api-details">
                        {Object.entries(call.details).map(([key, value]) => (
                          <div key={key} className="detail-item">
                            <span className="detail-key">{key}:</span>
                            <span className="detail-value">{JSON.stringify(value)}</span>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>

            <div className="performance-metrics">
              <h5>📊 Performance Metrics</h5>
              <div className="metrics-grid">
                {Object.entries(technicalDetails.metrics).map(([key, value]) => (
                  <div key={key} className="metric-item">
                    <div className="metric-label">{key.replace(/_/g, ' ').toUpperCase()}</div>
                    <div className="metric-value">{JSON.stringify(value)}</div>
                  </div>
                ))}
              </div>
            </div>

            <div className="system-info">
              <h5>🏗️ System Architecture</h5>
              <div className="architecture-flow">
                <div className="arch-step">🌐 API Gateway</div>
                <div className="arch-arrow">→</div>
                <div className="arch-step">⚡ AWS Lambda</div>
                <div className="arch-arrow">→</div>
                <div className="arch-step">🧠 Amazon Bedrock</div>
                <div className="arch-arrow">→</div>
                <div className="arch-step">🗄️ S3 Vectors</div>
              </div>
            </div>
          </div>
        )}
      </div>
    );
  };

  const ChatMessage = ({ message }) => {
    if (message.type === 'question') {
      return (
        <div className="message user-message">
          <div className="message-content">
            <MessageCircle className="message-icon" />
            <div className="message-text">{message.content}</div>
          </div>
          <div className="message-time">
            <Clock className="time-icon" />
            {new Date(message.timestamp).toLocaleTimeString()}
          </div>
        </div>
      );
    }
    
    if (message.type === 'error') {
      return (
        <div className="message error-message">
          <div className="message-content">
            <div className="message-text">{message.content}</div>
          </div>
        </div>
      );
    }
    
    return (
      <div className="message assistant-message">
        <div className="message-content">
          <BookOpen className="message-icon" />
          <div className="message-text">
            <ReactMarkdown
              components={{
                code({node, inline, className, children, ...props}) {
                  const match = /language-(\w+)/.exec(className || '');
                  return !inline && match ? (
                    <SyntaxHighlighter
                      style={tomorrow}
                      language={match[1]}
                      PreTag="div"
                      {...props}
                    >
                      {String(children).replace(/\n$/, '')}
                    </SyntaxHighlighter>
                  ) : (
                    <code className={className} {...props}>
                      {children}
                    </code>
                  );
                }
              }}
            >
              {message.content}
            </ReactMarkdown>
          </div>
        </div>
        
        {message.sources && message.sources.length > 0 && (
          <div className="message-sources">
            <h4>📚 Sources ({message.documentsRetrieved} documents retrieved):</h4>
            {message.sources.slice(0, 3).map((source, index) => (
              <div key={index} className="source-item">
                <ExternalLink className="source-icon" />
                <span className="source-text">
                  {source.service_name} - {source.document_type} 
                  <span className="similarity-score">({source.similarity_score}% similarity)</span>
                </span>
              </div>
            ))}
          </div>
        )}

        {message.technicalDetails && (
          <TechnicalDetailsPanel technicalDetails={message.technicalDetails} />
        )}
        
        <div className="message-meta">
          <div className="message-time">
            <Clock className="time-icon" />
            {new Date(message.timestamp).toLocaleTimeString()}
          </div>
          <div className="model-info">
            <Zap className="model-icon" />
            {message.modelUsed?.includes('claude') ? 'Claude 3.5 Sonnet' : 'AI Assistant'}
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <div className="header-title">
            <BookOpen className="header-icon" />
            <h1>AWS Documentation Assistant</h1>
          </div>
          <p className="header-subtitle">
            Ask questions about AWS services and get comprehensive answers powered by Claude 3.5 Sonnet
          </p>
        </div>
      </header>

      <main className="app-main">
        <div className="chat-container">
          {showExamples && chatHistory.length === 0 && <ExampleQuestions />}
          
          <div className="chat-history">
            {chatHistory.map((message) => (
              <ChatMessage key={message.id} message={message} />
            ))}
            
            {loading && (
              <div className="message loading-message">
                <div className="message-content">
                  <Loader className="loading-icon spinning" />
                  <div className="loading-text">
                    <div>🔍 Searching AWS documentation...</div>
                    <div>🧠 Generating comprehensive answer...</div>
                  </div>
                </div>
              </div>
            )}
            
            <div ref={chatEndRef} />
          </div>
        </div>

        <div className="input-section">
          {chatHistory.length > 0 && (
            <button className="clear-button" onClick={clearHistory}>
              <Trash2 className="clear-icon" />
              Clear History
            </button>
          )}
          
          <div className="input-container">
            <textarea
              className="question-input"
              placeholder="Ask me anything about AWS services... (e.g., How do I scale Lambda functions?)"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyPress={handleKeyPress}
              disabled={loading}
              rows={3}
            />
            <button 
              className="send-button"
              onClick={() => askQuestion()}
              disabled={loading || !question.trim()}
            >
              <Send className="send-icon" />
              {loading ? 'Thinking...' : 'Ask'}
            </button>
          </div>
        </div>
      </main>

      <div className="knowledge-domains">
        <div className="domains-header">
          <BookOpen className="domains-icon" />
          <h4>📚 Knowledge Base Coverage</h4>
        </div>
        <div className="domains-content">
          <p><strong>This AI assistant can answer questions about the following AWS domains:</strong></p>
          
          <div className="domains-grid">
            <div className="domain-category">
              <h5>🖥️ Compute Services</h5>
              <ul>
                <li>EC2 (Elastic Compute Cloud) - instances, scaling, optimization</li>
                <li>Lambda - serverless functions, event-driven computing</li>
                <li>ECS - containerized applications</li>
                <li>EKS - Kubernetes on AWS</li>
              </ul>
            </div>
            
            <div className="domain-category">
              <h5>💾 Storage & Database</h5>
              <ul>
                <li>S3 - object storage, storage classes, security</li>
                <li>DynamoDB - NoSQL database, performance optimization</li>
                <li>RDS - relational databases, backup & recovery</li>
              </ul>
            </div>
            
            <div className="domain-category">
              <h5>🌐 Networking & Content</h5>
              <ul>
                <li>VPC - virtual private clouds, networking</li>
                <li>Route 53 - DNS and domain management</li>
                <li>API Gateway - API management and deployment</li>
              </ul>
            </div>
            
            <div className="domain-category">
              <h5>📊 Monitoring & Messaging</h5>
              <ul>
                <li>CloudWatch - monitoring, logging, metrics</li>
                <li>SNS - notification service</li>
                <li>SQS - message queuing</li>
                <li>Kinesis - real-time data streaming</li>
              </ul>
            </div>
            
            <div className="domain-category">
              <h5>🔐 Security & Management</h5>
              <ul>
                <li>IAM - identity and access management, policies</li>
                <li>Security best practices and compliance</li>
                <li>CloudFormation - infrastructure as code</li>
              </ul>
            </div>
            
            <div className="domain-category">
              <h5>💰 Cost & Architecture</h5>
              <ul>
                <li>Cost optimization strategies and best practices</li>
                <li>Well-Architected Framework principles</li>
                <li>Service selection and architecture guidance</li>
              </ul>
            </div>
          </div>
          
          <div className="domains-note">
            <p><em>💡 Knowledge base contains <strong>139 documentation chunks</strong> covering core AWS services. 
            For the most current information on newer services or recent updates, please refer to the official AWS documentation.</em></p>
          </div>
        </div>
      </div>

      <footer className="app-footer">
        <p>Powered by Amazon S3 Vectors, Claude 3.5 Sonnet, and Titan Text Embeddings V2</p>
      </footer>
    </div>
  );
}

export default App;
