import React from 'react';
import './Header.css';

function Header({ user }) {
  return (
    <header className="header">
      <div className="header-left">
        <h1>📰 AI News Summarizer</h1>
        <p>Real-time news with intelligent summaries</p>
      </div>
      <div className="header-right">
        <div className="user-info">
          <div className="user-avatar">
            {user.name.charAt(0)}
          </div>
          <span className="user-name">{user.name}</span>
        </div>
      </div>
    </header>
  );
}

export default Header;