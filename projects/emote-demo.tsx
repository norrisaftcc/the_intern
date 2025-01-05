import React from 'react';

const EmoteDemo = () => {
  const emoteText = "projects a holographic example of how content flows through this structure";
  const timestamp = new Date().toLocaleTimeString();
  
  // Circuit's theme color - a bright, electric blue
  const circuitTheme = {
    primary: '#4A90E2',
    background: '#4A90E220'
  };

  return (
    <div className="w-64 p-4 bg-gray-100">
      <h3 className="font-bold mb-4">Circuit's Actions</h3>
      <div 
        className="p-2 rounded mb-2"
        style={{ backgroundColor: circuitTheme.background }}
      >
        <div className="text-xs text-gray-500">{timestamp}</div>
        <div style={{ color: circuitTheme.primary }}>
          [*{emoteText}*]
        </div>
      </div>
    </div>
  );
};

export default EmoteDemo;