import React, { useState } from 'react';
import HomePage from './pages/HomePage';
import HowItWorksPage from './pages/HowItWorksPage';

function App() {
  const [route, setRoute] = useState('home');

  return (
    <div className="App">
      <nav className="nav" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: 12, padding: '12px 16px' }}>
        <div style={{ display: 'flex', gap: 12 }}>
          <button type="button" className="page-btn" onClick={() => setRoute('home')}>
            Home
          </button>
          <button type="button" className="page-btn" onClick={() => setRoute('how')}>
            How it works
          </button>
        </div>
        <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
          <a href="https://github.com/adityakamath1997" target="_blank" rel="noopener noreferrer" className="page-btn">
            GitHub
          </a>
          <span className="made-with">Made with <span className="heart">♥</span> by Aditya</span>
        </div>
      </nav>

      {route === 'home' && <HomePage />}
      {route === 'how' && <HowItWorksPage onBackToHome={() => setRoute('home')} />}
    </div>
  );
}

export default App;
