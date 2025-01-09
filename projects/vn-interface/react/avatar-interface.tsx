import React, { useState, useEffect } from 'react';
import { Card } from '@/components/ui/card';

const AvatarInterface = () => {
  // This would be expanded with all possible avatar states
  const avatarStates = {
    default: '/api/placeholder/200/300',  // Standing pose
    thinking: '/api/placeholder/200/300', // Hand on chin
    excited: '/api/placeholder/200/300',  // Energetic pose
    teaching: '/api/placeholder/200/300'  // Pointing to holographic display
  };

  const [currentState, setCurrentState] = useState('default');
  const [emoteLog, setEmoteLog] = useState([]);

  // Example of how we could parse messages to update avatar state
  const processMessage = (message, emote) => {
    // Add emote to the sidebar log
    const newEmote = {
      timestamp: new Date().toLocaleTimeString(),
      action: emote,
      color: '#4A90E2' // Circuit's theme color
    };
    setEmoteLog([newEmote, ...emoteLog]);

    // Update avatar state based on emote content
    if (emote.includes('adjusts glasses')) {
      setCurrentState('thinking');
    } else if (emote.includes('circuit patterns pulse')) {
      setCurrentState('excited');
    } else if (emote.includes('projects holographic')) {
      setCurrentState('teaching');
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
              alt="Circuit Chen"
              className="w-full h-auto"
            />
          </div>
          
          {/* Main content would go here */}
          <div className="pr-72">
            <Card className="p-4">
              <p>"Remember students... make sure you always have an even number of parentheses in your Python code!"</p>
            </Card>
          </div>
        </div>
      </div>

      {/* Emote sidebar */}
      <div className="w-64 bg-gray-100 p-4 overflow-y-auto">
        <h3 className="font-bold mb-4">Circuit's Actions</h3>
        {emoteLog.map((emote, index) => (
          <div 
            key={index} 
            className="mb-2 p-2 rounded"
            style={{ backgroundColor: `${emote.color}20` }}
          >
            <div className="text-xs text-gray-500">{emote.timestamp}</div>
            <div style={{ color: emote.color }}>{emote.action}</div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AvatarInterface;