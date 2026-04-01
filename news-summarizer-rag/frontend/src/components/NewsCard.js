import React from 'react';
import './NewsCard.css';

function NewsCard({ article, summary, onSummarize, ragEnabled }) {
  const formatDate = (dateString) => {
    if (!dateString) return 'Recently';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getCategoryColor = (category) => {
    const colors = {
      technology: '#4caf50',
      business: '#ff9800',
      health: '#f44336',
      sports: '#2196f3',
      politics: '#9c27b0',
      general: '#607d8b'
    };
    return colors[category] || '#607d8b';
  };

  return (
    <div className="news-card fade-in">
      <div className="card-header">
        <span className="category" style={{ backgroundColor: getCategoryColor(article.category) }}>
          {article.category || 'General'}
        </span>
        <span className="date">{formatDate(article.published_at)}</span>
      </div>
      
      <h3 className="card-title">{article.title}</h3>
      
      <p className="card-description">
        {article.description || 'No description available'}
      </p>
      
      <div className="card-footer">
        <div className="source-info">
          <span className="source">{article.source}</span>
        </div>
        <div className="card-actions">
          <button className="summarize-btn" onClick={onSummarize}>
            🤖 Generate Summary
          </button>
          <a href={article.url} target="_blank" rel="noopener noreferrer" className="read-more">
            Read More →
          </a>
        </div>
      </div>
      
      {summary && (
        <div className="summary-container">
          <div className="summary-header">
            <span>📝 AI Summary {ragEnabled && '(with RAG Context)'}</span>
          </div>
          <p className="summary-text">{summary}</p>
        </div>
      )}
    </div>
  );
}

export default NewsCard;