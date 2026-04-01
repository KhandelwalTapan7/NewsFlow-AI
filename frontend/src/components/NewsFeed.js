import React, { useState } from 'react';
import axios from 'axios';
import { toast } from 'react-hot-toast';
import NewsCard from './NewsCard';
import './NewsFeed.css';

const API_BASE_URL = 'http://localhost:8000/api/v1';

function NewsFeed({ news, loading, onRefresh, onSearch, userId, ragEnabled }) {
  const [searchQuery, setSearchQuery] = useState('');
  const [summaries, setSummaries] = useState({});

  const handleSearch = () => {
    if (searchQuery.trim()) {
      onSearch(searchQuery);
    }
  };

  const handleSummarize = async (articleId, content) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/summarize`, {
        content: content,
        article_id: articleId,
        user_id: userId,
        rag_enabled: ragEnabled
      });
      
      setSummaries({ ...summaries, [articleId]: response.data.summary });
      toast.success('Summary generated!');
    } catch (error) {
      toast.error('Failed to summarize');
    }
  };

  return (
    <div className="news-feed">
      <div className="feed-header">
        <div className="search-bar">
          <input
            type="text"
            placeholder="Search news by topic..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
          />
          <button onClick={handleSearch}>🔍 Search</button>
        </div>
        <button className="refresh-btn" onClick={onRefresh}>
          🔄 Refresh
        </button>
      </div>

      {loading ? (
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Fetching latest news...</p>
        </div>
      ) : (
        <div className="news-grid">
          {news && news.length > 0 ? (
            news.map((article, index) => (
              <NewsCard
                key={article.id || index}
                article={article}
                summary={summaries[article.id]}
                onSummarize={() => handleSummarize(article.id, article.content || article.description)}
                ragEnabled={ragEnabled}
              />
            ))
          ) : (
            <div className="no-news">
              <p>No news articles found. Try refreshing or changing your preferences.</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default NewsFeed;