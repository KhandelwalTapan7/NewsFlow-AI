import React, { useState } from 'react';
import './Auth.css';

function Onboarding({ onComplete }) {
  const [step, setStep] = useState(0);

  const steps = [
    {
      icon: '📬',
      title: 'Welcome to NewsFlow AI!',
      description: 'Your intelligent news companion that summarizes articles and provides personalized insights.'
    },
    {
      icon: '🤖',
      title: 'AI-Powered Summaries',
      description: 'Get concise, easy-to-read summaries of news articles. RAG technology provides historical context for deeper understanding.'
    },
    {
      icon: '🎯',
      title: 'Personalized Feed',
      description: 'Select your interests to get news tailored just for you. Our AI learns your preferences over time.'
    },
    {
      icon: '📊',
      title: 'Track Your Reading',
      description: 'View statistics about your reading habits and discover new topics you might enjoy.'
    }
  ];

  const handleNext = () => {
    if (step < steps.length - 1) {
      setStep(step + 1);
    } else {
      onComplete();
    }
  };

  const handleSkip = () => {
    onComplete();
  };

  return (
    <div className="onboarding-container">
      <div className="onboarding-card">
        <div className="step-indicator">
          {steps.map((_, idx) => (
            <div
              key={idx}
              className={`step-dot ${idx === step ? 'active' : ''} ${idx < step ? 'completed' : ''}`}
            />
          ))}
        </div>
        
        <div className="onboarding-step">
          <div className="onboarding-icon">{steps[step].icon}</div>
          <h2>{steps[step].title}</h2>
          <p>{steps[step].description}</p>
          
          <div className="onboarding-buttons">
            <button className="btn-skip" onClick={handleSkip}>
              Skip Tutorial
            </button>
            <button className="btn-next" onClick={handleNext}>
              {step === steps.length - 1 ? 'Get Started' : 'Next'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Onboarding;