import React, { useState } from 'react';
import HomePage from './pages/HomePage';
import HowItWorksPage from './pages/HowItWorksPage';

function App() {
  const [route, setRoute] = useState('home');

  return (
    <div className="App">
      <nav className="nav" style={{ display: 'flex', gap: 12, padding: '12px 16px' }}>
        <button type="button" className="page-btn" onClick={() => setRoute('home')}>
          Home
        </button>
        <button type="button" className="page-btn" onClick={() => setRoute('how')}>
          How it works
        </button>
      </nav>

      {route === 'home' && <HomePage />}
      {route === 'how' && <HowItWorksPage onBackToHome={() => setRoute('home')} />}
    </div>
  );
}

export default App;
