import React, { useState, useEffect } from "react";
import axios from 'axios';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import userAvatar from '../images/user-avatar.png'; // Adjust the path as needed
import aiAvatar from '../images/ai-avatar.png'; // Adjust the path as needed
import { ArrowUp } from 'react-bootstrap-icons';

const MiddlePanel = () => {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [suggestions, setSuggestions] = useState([
    "Ni hao!",
    "Wo shi xuesheng. Ni ne?",
    "Wo jiao Esther! Ni ne?",
    "Ni hao, wo jiao Esther. Wo shi xuesheng. Ni ne?",
  ]); // These are example suggestions, adjust as needed
  const baseURLMain = "http://127.0.0.1:5001"; // Your API base URL

  // Fetch messages from the backend
  const fetchMessages = async () => {
    try {
      const response = await axios.get(`${baseURLMain}/messages`);
      // Ensure you adjust this according to the new response structure from your backend
      setMessages(response.data.data); // This might need adjustment
    } catch (error) {
      console.error("Error fetching messages:", error);
    }
  };

  useEffect(() => {
    fetchMessages();
  }, []);

  const handleMessageChange = (e) => {
    setMessage(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Ensure you adjust the request payload if needed to match the new backend's expectations
      await axios.post(`${baseURLMain}/messages`, { message: message });
      setMessage(""); // Clear the message input
      fetchMessages(); // Re-fetch messages to display the new one
    } catch (error) {
      console.error("Error sending message:", error);
    }
  };

  const handleSuggestionClick = (suggestion) => {
    setMessage(suggestion); // Set the clicked suggestion as the message
  };

  return (
    <div>
      
      <div style={{ height: '60vh', overflowY: 'scroll' }}>
        {/* Display messages */}
        {messages.map((msg, index) => (
          <div key={index} style={{ display: 'flex', alignItems: 'center', marginBottom: '10px' }}>
            <img 
              src={msg.role === "user" ? userAvatar : aiAvatar}
              alt="Avatar"
              style={{ width: '40px', height: '40px', borderRadius: '50%', marginRight: '10px' }}
            />
            <div>
              <h4>{msg.role === "system" ? "AI" : "You"}</h4>
              <p>{msg.content}</p>
            </div>
          </div>
        ))}
      </div>

      <div style={{ display: 'flex', justifyContent: 'space-around', padding: '10px' }}>
        {suggestions.map((suggestion, index) => (
          <Button style={{ margin: '3px' }} key={index} variant="light" onClick={() => handleSuggestionClick(suggestion)}>
            {suggestion}
          </Button>
        ))}
      </div>

      {/* Message input form */}
      <Form onSubmit={handleSubmit}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <Form.Group className="mb-3" style={{ flexGrow: 1 }}>
            <Form.Label>Message</Form.Label>
            <Form.Control as="textarea" rows={3} value={message} onChange={handleMessageChange} />
          </Form.Group>
          <Button variant="primary" type="submit" style={{ height: 'fit-content' }}>
            <ArrowUp /> {/* Icon */}
          </Button>
        </div>
      </Form>
    </div>
  );
};

export default MiddlePanel;
