import React, { useState } from 'react';
import './Preferences.css';

const AVAILABLE_TOPICS = [
  'technology', 'politics', 'business', 'health', 
  'sports', 'science', 'entertainment'
];

function Preferences({ interests, onUpdate, ragEnabled, onToggleRAG }) {
  const [selectedTopics, setSelectedTopics] = useState(interests);

  const toggleTopic = (topic) => {
    if (selectedTopics.includes(topic)) {
      setSelectedTopics(selectedTopics.filter(t => t !== topic));
    } else {
      if (selectedTopics.length < 5) {
        setSelectedTopics([...selectedTopics, topic]);
      } else {
        alert('You can select up to 5 interests only');
      }
    }
  };

  const handleSave = () => {
    if (selectedTopics.length === 0) {
      alert('Please select at least one interest');
      return;
    }
    onUpdate(selectedTopics);
  };

  return (
    <div className="preferences-container fade-in">
      <div className="preferences-card">
        <h2>🎯 Customize Your News Feed</h2>
        <p>Select topics that interest you (max 5)</p>
        
        <div className="topics-grid">
          {AVAILABLE_TOPICS.map(topic => (
            <div
              key={topic}
              className={`topic-chip ${selectedTopics.includes(topic) ? 'selected' : ''}`}
              onClick={() => toggleTopic(topic)}
            >
              {topic.charAt(0).toUpperCase() + topic.slice(1)}
            </div>
          ))}
        </div>
        
        <button className="save-btn" onClick={handleSave}>
          Save Preferences
        </button>
      </div>

      <div className="settings-card">
        <h3>⚙️ Advanced Settings</h3>
        <div className="setting-item">
          <div className="setting-info">
            <span className="setting-name">RAG (Retrieval-Augmented Generation)</span>
            <span className="setting-description">
              Enable historical context for better summaries
            </span>
          </div>
          <label className="switch">
            <input type="checkbox" checked={ragEnabled} onChange={onToggleRAG} />
            <span className="slider"></span>
          </label>
        </div>
      </div>
    </div>
  );
}

export default Preferences;