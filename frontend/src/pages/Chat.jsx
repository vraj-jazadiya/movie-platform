import React, { useState, useEffect, useContext } from 'react';
import { chatAPI } from '../services/api';
import { AuthContext } from '../App';

const Chat = () => {
  const { user } = useContext(AuthContext);
  const [chat, setChat] = useState(null);
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);

  useEffect(() => {
    fetchChat();
  }, []);

  const fetchChat = async () => {
    try {
      setLoading(true);
      const response = await chatAPI.getMyChat();
      setChat(response.data);
      setMessages(response.data.messages || []);
    } catch (error) {
      console.error('Error fetching chat:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!newMessage.trim() || !chat) return;

    try {
      setSending(true);
      await chatAPI.sendMessage(chat._id, newMessage);
      setMessages([...messages, {
        sender: user._id,
        message: newMessage,
        timestamp: new Date().toISOString()
      }]);
      setNewMessage('');
      fetchChat(); // Refresh to get updated messages
    } catch (error) {
      console.error('Error sending message:', error);
    } finally {
      setSending(false);
    }
  };

  if (loading) {
    return (
      <div className="container">
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Loading chat...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="chat-page">
      <div className="container">
        <div className="chat-container">
          <div className="chat-header">
            <h1 className="chat-title">💬 Chat with Admin</h1>
            <p className="chat-subtitle">Get help and support from our team</p>
          </div>

          <div className="chat-box">
            <div className="messages-container">
              {messages.length > 0 ? (
                messages.map((msg, index) => (
                  <div 
                    key={index} 
                    className={`message ${msg.sender === user._id ? 'message-sent' : 'message-received'}`}
                  >
                    <div className="message-content">
                      <p>{msg.message}</p>
                      <span className="message-time">
                        {new Date(msg.timestamp).toLocaleTimeString()}
                      </span>
                    </div>
                  </div>
                ))
              ) : (
                <div className="empty-chat">
                  <p>No messages yet. Start a conversation!</p>
                </div>
              )}
            </div>

            <form onSubmit={handleSendMessage} className="message-input-form">
              <input
                type="text"
                value={newMessage}
                onChange={(e) => setNewMessage(e.target.value)}
                placeholder="Type your message..."
                className="message-input"
                disabled={sending}
              />
              <button 
                type="submit" 
                className="btn btn-primary"
                disabled={sending || !newMessage.trim()}
              >
                {sending ? 'Sending...' : 'Send'}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Chat;
