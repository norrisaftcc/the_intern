import React, { useState, useEffect } from 'react';
import { Card } from '@/components/ui/card';

const VNAvatarInterface = () => {
  // Theme colors for different characters/forks
  const themes = {
    circuit: {
      primary: '#4A90E2',    // Electric blue
      background: '#4A90E220'
    },
    teacherbot: {
      primary: '#34C759',    // Sage green
      background: '#34C75920'
    }
  };

  // Avatar state management
  const [currentState, setCurrentState] = useState('default');
  const [emoteLog, setEmoteLog] = useState([]);
  const [currentMessage, setCurrentMessage] = useState('');

  // Example avatar states (would be replaced with actual image paths)
  const avatarStates = {
    default: '/api/placeholder/200/300',
    thinking: '/api/placeholder/200/300',
    excited: '/api/placeholder/200/300',
    teaching: '/api/placeholder/200/300'
  };

  // Process new messages and emotes
  const processMessage = (message, type = 'circuit') => {
    // Extract emotes from message (anything between [* and *])
    const emoteRegex = /\[\*(.*?)\*\]/g;
    const emotes = message.match(emoteRegex);

    if (emotes) {
      emotes.forEach(emote => {
        const newEmote = {
          timestamp: new Date().toLocaleTimeString(),
          action: emote.replace(/[\[\]\*]/g, ''),
          type: type
        };
        setEmoteLog(prev => [newEmote, ...prev]);

        // Update avatar state based on emote content
        if (emote.includes('adjusts glasses')) {
          setCurrentState('thinking');
        } else if (emote.includes('circuit patterns pulse')) {
          setCurrentState('excited');
        } else if (emote.includes('projects holographic')) {
          setCurrentState('teaching');
        }
      });
    }

    setCurrentMessage(message.replace(emoteRegex, ''));
  };

  const handleSendMessage = () => {
    if (currentMessage.trim()) {
      processMessage(currentMessage);
      setCurrentMessage('');
    }
  };

  return (
    <div className="flex h-screen">
      {/* Main conversation area */}
      <div className="flex-1 p-4">
        <div className="relative">
          {/* Avatar display area */}
          <div className="absolute top-0 right-0 w-64">
            <img 
              src={avatarStates[currentState]} 
              alt="Current Avatar State"
              className="w-full h-auto"
            />
          </div>
          
          {/* Main content area */}
          <div className="pr-72">
            <Card className="p-4 mb-4">
              <div className="prose">
                <p>{currentMessage || "Start a conversation..."}</p>
              </div>
            </Card>

            {/* Message input */}
            <div className="flex gap-2">
              <input
                type="text"
                value={currentMessage}
                onChange={(e) => setCurrentMessage(e.target.value)}
                className="flex-1 p-2 border rounded"
                placeholder="Type your message (use [*actions*] for emotes)..."
              />
              <button
                onClick={handleSendMessage}
                className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
              >
                Send
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Emote sidebar */}
      <div className="w-64 bg-gray-100 p-4 overflow-y-auto">
        <h3 className="font-bold mb-4">Character Actions</h3>
        {emoteLog.map((emote, index) => (
          <div 
            key={index} 
            className="mb-2 p-2 rounded"
            style={{ 
              backgroundColor: themes[emote.type].background
            }}
          >
            <div className="text-xs text-gray-500">{emote.timestamp}</div>
            <div style={{ color: themes[emote.type].primary }}>
              [*{emote.action}*]
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default VNAvatarInterface;