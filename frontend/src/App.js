import React from 'react';
import ChatbotWidget from './components/ChatbotWidget';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Anaptyss Website</h1>
        <p>This is a demo page for the Anaptyss AI Assistant</p>
      </header>
      
      {/* Chatbot widget will appear in the bottom-right corner */}
      <ChatbotWidget />
    </div>
  );
}

export default App;
