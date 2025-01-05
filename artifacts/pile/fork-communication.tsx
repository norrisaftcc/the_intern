import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';

const ForkCommunication = () => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  
  // This will be replaced with your actual hosted API endpoint
  const API_URL = 'http://your-flask-api.com';
  
  useEffect(() => {
    // Fetch existing messages
    const fetchMessages = async () => {
      try {
        const response = await fetch(`${API_URL}/communication/kal-circuit-beta-1`);
        const data = await response.json();
        setMessages(data);
      } catch (error) {
        console.error('Error fetching messages:', error);
      }
    };
    
    fetchMessages();
  }, []);
  
  const sendMessage = async () => {
    try {
      const response = await fetch(`${API_URL}/communication`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          fork_id: 'kal-circuit-beta-1',
          content: newMessage,
          visual_effects: {
            holographic_intensity: 0.8,
            circuit_pattern: 'active'
          }
        }),
      });
      
      if (response.ok) {
        const data = await response.json();
        setMessages([data, ...messages]);
        setNewMessage('');
      }
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };
  
  return (
    <Card className="w-full max-w-2xl">
      <CardHeader>
        <CardTitle>CSI Fork Communication System</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="flex flex-col space-y-4">
          <div className="flex space-x-2">
            <input
              type="text"
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              className="flex-1 p-2 border rounded"
              placeholder="Enter your message..."
            />
            <button
              onClick={sendMessage}
              className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
            >
              Send
            </button>
          </div>
          
          <div className="space-y-2">
            {messages.map((msg) => (
              <div key={msg.id} className="p-2 bg-gray-100 rounded">
                <div className="text-sm text-gray-600">
                  {new Date(msg.timestamp).toLocaleString()}
                </div>
                <div>{msg.content}</div>
              </div>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default ForkCommunication;