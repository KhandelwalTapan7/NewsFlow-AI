import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Toaster, toast } from 'react-hot-toast';
import Auth from './Auth';
import Onboarding from './Onboarding';
import './App.css';

const API_BASE_URL = 'http://localhost:8000';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [showOnboarding, setShowOnboarding] = useState(false);
  const [user, setUser] = useState(null);
  const [activeTab, setActiveTab] = useState('feed');
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedSource, setSelectedSource] = useState('all');
  const [sortBy, setSortBy] = useState('latest');
  const [stats, setStats] = useState({
    totalRead: 0,
    interests: [],
    ragEnabled: true
  });
  const [summaries, setSummaries] = useState({});
  const [showFilters, setShowFilters] = useState(false);
  const [viewMode, setViewMode] = useState('grid');
  const [greeting, setGreeting] = useState('');

  const categories = [
    { id: 'all', name: 'All News', icon: '🌐', color: '#667eea' },
    { id: 'technology', name: 'Technology', icon: '💻', color: '#4caf50' },
    { id: 'politics', name: 'Politics', icon: '🏛️', color: '#f39c12' },
    { id: 'business', name: 'Business', icon: '📊', color: '#2ecc71' },
    { id: 'health', name: 'Health', icon: '🏥', color: '#e74c3c' },
    { id: 'sports', name: 'Sports', icon: '⚽', color: '#3498db' },
    { id: 'science', name: 'Science', icon: '🔬', color: '#9b59b6' },
    { id: 'entertainment', name: 'Entertainment', icon: '🎬', color: '#e84393' }
  ];

  const sources = [
    { id: 'all', name: 'All Sources' },
    { id: 'NewsAPI', name: 'NewsAPI' },
    { id: 'Guardian', name: 'The Guardian' },
    { id: 'NewsData.io', name: 'NewsData.io' },
    { id: 'World News API', name: 'World News' }
  ];

  useEffect(() => {
    // Check if user is logged in
    const token = localStorage.getItem('token');
    const savedUser = localStorage.getItem('user');
    
    if (token && savedUser) {
      const userData = JSON.parse(savedUser);
      setUser(userData);
      setIsAuthenticated(true);
      
      // Check if onboarding was completed
      const onboardingCompleted = localStorage.getItem('onboardingCompleted');
      if (!onboardingCompleted) {
        setShowOnboarding(true);
      } else {
        fetchNews();
        fetchStats();
        setGreeting(getGreeting());
      }
    }
  }, []);

  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return 'Good Morning';
    if (hour < 18) return 'Good Afternoon';
    return 'Good Evening';
  };

  const fetchNews = async (type = 'personalized', query = '', category = null) => {
    setLoading(true);
    try {
      let url = '';
      const token = localStorage.getItem('token');
      
      if (category && category !== 'all') {
        url = `${API_BASE_URL}/api/v1/news/category/${category}?limit=50`;
      } else if (type === 'personalized') {
        url = `${API_BASE_URL}/api/v1/news/personalized/${user.id}?limit=50`;
      } else if (type === 'search' && query) {
        url = `${API_BASE_URL}/api/v1/news/search?q=${encodeURIComponent(query)}&limit=50`;
      } else {
        url = `${API_BASE_URL}/api/v1/news/all?limit=50`;
      }
      
      const headers = token ? { Authorization: `Bearer ${token}` } : {};
      const response = await axios.get(url, { headers });
      
      if (response.data && response.data.success !== false) {
        let articles = response.data.articles || [];
        
        if (selectedSource !== 'all') {
          articles = articles.filter(a => a.source === selectedSource);
        }
        
        if (sortBy === 'latest') {
          articles.sort((a, b) => new Date(b.published_at) - new Date(a.published_at));
        } else if (sortBy === 'oldest') {
          articles.sort((a, b) => new Date(a.published_at) - new Date(b.published_at));
        }
        
        setNews(articles);
        
        if (articles.length === 0) {
          toast('No articles found', { icon: '📭' });
        } else {
          toast.success(`📰 ${articles.length} articles loaded`);
        }
      }
    } catch (error) {
      console.error('Error fetching news:', error);
      if (error.response?.status === 401) {
        handleLogout();
      } else {
        toast.error('Failed to fetch news');
      }
    } finally {
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_BASE_URL}/api/v1/user/${user?.id}/stats`, {
        headers: token ? { Authorization: `Bearer ${token}` } : {}
      });
      if (response.data) {
        setStats({
          totalRead: response.data.totalRead || 0,
          interests: response.data.interests || user?.interests || [],
          ragEnabled: response.data.ragEnabled !== undefined ? response.data.ragEnabled : true
        });
      }
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  const generateSummary = async (articleId, content) => {
    if (summaries[articleId]) {
      delete summaries[articleId];
      setSummaries({ ...summaries });
      return;
    }
    
    toast.loading('🤖 Generating AI summary...', { id: 'summary' });
    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(`${API_BASE_URL}/api/v1/summarize`, {
        article_id: articleId,
        content: content,
        user_id: user.id,
        rag_enabled: stats.ragEnabled
      }, {
        headers: token ? { Authorization: `Bearer ${token}` } : {}
      });
      
      if (response.data && response.data.summary) {
        setSummaries({ ...summaries, [articleId]: response.data.summary });
        toast.success('✨ Summary generated!', { id: 'summary' });
      }
    } catch (error) {
      console.error('Error generating summary:', error);
      toast.error('Failed to generate summary', { id: 'summary' });
    }
  };

  const handleLogin = (userData) => {
    setUser(userData);
    setIsAuthenticated(true);
    setShowOnboarding(true);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    localStorage.removeItem('onboardingCompleted');
    setIsAuthenticated(false);
    setUser(null);
    toast.success('Logged out successfully');
  };

  const handleOnboardingComplete = () => {
    localStorage.setItem('onboardingCompleted', 'true');
    setShowOnboarding(false);
    fetchNews();
    fetchStats();
    setGreeting(getGreeting());
  };

  const handleCategoryClick = (categoryId) => {
    setSelectedCategory(categoryId);
    setActiveTab('feed');
    
    if (categoryId === 'all') {
      fetchNews('all', '', null);
    } else {
      fetchNews('category', '', categoryId);
    }
  };

  const handleSearch = () => {
    if (searchQuery.trim()) {
      setSelectedCategory('all');
      fetchNews('search', searchQuery);
      setActiveTab('feed');
    }
  };

  const updateInterests = async () => {
    const interestsInput = prompt(
      'Select your interests (comma-separated):\n\nAvailable: technology, politics, business, health, sports, science, entertainment\n\nCurrent: ' + (user?.interests?.join(', ') || ''),
      user?.interests?.join(', ') || ''
    );
    
    if (interestsInput) {
      const interests = interestsInput.split(',').map(i => i.trim().toLowerCase());
      const validInterests = interests.filter(i => 
        ['technology', 'politics', 'business', 'health', 'sports', 'science', 'entertainment'].includes(i)
      );
      
      if (validInterests.length === 0) {
        toast.error('Please select at least one valid interest');
        return;
      }
      
      try {
        const token = localStorage.getItem('token');
        await axios.post(`${API_BASE_URL}/api/v1/user/${user.id}/interests`, 
          { interests: validInterests },
          { headers: token ? { Authorization: `Bearer ${token}` } : {} }
        );
        setUser({ ...user, interests: validInterests });
        setStats({ ...stats, interests: validInterests });
        toast.success('🎯 Interests updated!');
        fetchNews('personalized');
      } catch (error) {
        toast.error('Failed to update interests');
      }
    }
  };

  const toggleRAG = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(`${API_BASE_URL}/api/v1/settings/toggle-rag`, {}, {
        headers: token ? { Authorization: `Bearer ${token}` } : {}
      });
      setStats({ ...stats, ragEnabled: response.data.ragEnabled });
      toast.success(`RAG ${response.data.ragEnabled ? 'enabled' : 'disabled'}`);
    } catch (error) {
      toast.error('Failed to toggle RAG');
    }
  };

  const getCategoryIcon = (category) => {
    const cat = categories.find(c => c.id === category);
    return cat ? cat.icon : '📰';
  };

  const getCategoryColor = (category) => {
    const cat = categories.find(c => c.id === category);
    return cat ? cat.color : '#95a5a6';
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Recently';
    try {
      const date = new Date(dateString);
      const now = new Date();
      const diff = now - date;
      const minutes = Math.floor(diff / 60000);
      const hours = Math.floor(minutes / 60);
      const days = Math.floor(hours / 24);
      
      if (minutes < 1) return 'Just now';
      if (minutes < 60) return `${minutes}m ago`;
      if (hours < 24) return `${hours}h ago`;
      if (days < 7) return `${days}d ago`;
      return date.toLocaleDateString();
    } catch (e) {
      return 'Recently';
    }
  };

  // Show auth page if not authenticated
  if (!isAuthenticated) {
    return <Auth onLogin={handleLogin} />;
  }

  // Show onboarding if needed
  if (showOnboarding) {
    return <Onboarding onComplete={handleOnboardingComplete} />;
  }

  return (
    <div className="app">
      <Toaster position="top-right" />
      
      {/* Sidebar */}
      <div className="sidebar">
        <div className="sidebar-header">
          <div className="logo">
            <span className="logo-icon">📬</span>
            <span className="logo-text">NewsFlow AI</span>
          </div>
          <p className="tagline">Intelligent News Aggregator</p>
        </div>
        
        <nav className="sidebar-nav">
          <div 
            className={`nav-item ${activeTab === 'feed' ? 'active' : ''}`}
            onClick={() => setActiveTab('feed')}
          >
            <span className="nav-icon">📰</span>
            <span>News Feed</span>
          </div>
          <div 
            className={`nav-item ${activeTab === 'stats' ? 'active' : ''}`}
            onClick={() => setActiveTab('stats')}
          >
            <span className="nav-icon">📊</span>
            <span>Statistics</span>
          </div>
        </nav>
        
        <div className="sidebar-footer">
          <div className="user-info">
            <div className="user-avatar">{user?.name?.charAt(0) || 'U'}</div>
            <div className="user-details">
              <div className="user-name">{user?.name || 'User'}</div>
              <div className="user-interests">{user?.interests?.length || 0} interests</div>
            </div>
          </div>
          <button className="logout-btn" onClick={handleLogout}>
            🚪 Logout
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="main-content">
        {/* Header */}
        <header className="header">
          <div className="header-left">
            <h1>{greeting}, {user?.name?.split(' ')[0]}! 👋</h1>
            <p>Your personalized news feed with intelligent summaries</p>
          </div>
          <div className="header-right">
            <button className="icon-btn" onClick={() => setShowFilters(!showFilters)} title="Filters">
              🔍
            </button>
            <button className="icon-btn" onClick={updateInterests} title="Update Interests">
              🎯
            </button>
            <button className="icon-btn" onClick={toggleRAG} title={`RAG: ${stats.ragEnabled ? 'ON' : 'OFF'}`}>
              🧠
            </button>
            <button className="icon-btn" onClick={() => fetchNews('personalized')} title="Refresh">
              🔄
            </button>
          </div>
        </header>

        {/* Search Bar */}
        <div className="search-section">
          <div className="search-container">
            <input
              type="text"
              placeholder="Search news by topic, keyword, or event..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
              className="search-input"
            />
            <button onClick={handleSearch} className="search-button">
              🔍 Search
            </button>
          </div>
        </div>

        {/* Categories Bar */}
        <div className="categories-bar">
          {categories.map(cat => (
            <div
              key={cat.id}
              className={`category-chip ${selectedCategory === cat.id ? 'active' : ''}`}
              onClick={() => handleCategoryClick(cat.id)}
            >
              <span className="category-icon">{cat.icon}</span>
              <span className="category-name">{cat.name}</span>
            </div>
          ))}
        </div>

        {/* Filters Bar */}
        {showFilters && (
          <div className="filters-bar">
            <div className="filter-group">
              <label>Source:</label>
              <select value={selectedSource} onChange={(e) => setSelectedSource(e.target.value)}>
                {sources.map(s => (
                  <option key={s.id} value={s.id}>{s.name}</option>
                ))}
              </select>
            </div>
            <div className="filter-group">
              <label>Sort by:</label>
              <select value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
                <option value="latest">Latest First</option>
                <option value="oldest">Oldest First</option>
              </select>
            </div>
            <div className="filter-group">
              <label>View:</label>
              <div className="view-toggle">
                <button 
                  className={`view-btn ${viewMode === 'grid' ? 'active' : ''}`}
                  onClick={() => setViewMode('grid')}
                >⊞ Grid</button>
                <button 
                  className={`view-btn ${viewMode === 'list' ? 'active' : ''}`}
                  onClick={() => setViewMode('list')}
                >≡ List</button>
              </div>
            </div>
            <button className="apply-filters" onClick={() => {
              if (selectedCategory !== 'all') {
                fetchNews('category', '', selectedCategory);
              } else if (searchQuery) {
                fetchNews('search', searchQuery);
              } else {
                fetchNews('personalized');
              }
            }}>Apply Filters</button>
            <button className="reset-filters" onClick={() => {
              setSearchQuery('');
              setSelectedCategory('all');
              setSelectedSource('all');
              setSortBy('latest');
              fetchNews('personalized');
            }}>Reset</button>
          </div>
        )}

        {/* Content Area */}
        <div className="content-area">
          {activeTab === 'feed' && (
            <>
              {loading ? (
                <div className="loading-container">
                  <div className="spinner"></div>
                  <p>Fetching the latest news from all sources...</p>
                </div>
              ) : (
                <div className={`news-${viewMode}`}>
                  {news.length > 0 ? (
                    news.map((article, index) => (
                      <div key={article.id || index} className={`news-card ${viewMode === 'list' ? 'list-card' : ''}`}>
                        <div className="card-badge" style={{ backgroundColor: getCategoryColor(article.category) }}>
                          {getCategoryIcon(article.category)} {article.category || 'News'}
                        </div>
                        <h3 className="card-title">{article.title}</h3>
                        <p className="card-description">{article.description || 'No description available'}</p>
                        <div className="card-meta">
                          <span className="card-source">📡 {article.source}</span>
                          <span className="card-date">🕒 {formatDate(article.published_at)}</span>
                        </div>
                        <div className="card-actions">
                          <button 
                            className="btn-summarize"
                            onClick={() => generateSummary(article.id || index, article.content || article.description)}
                          >
                            {summaries[article.id || index] ? '📝 Hide Summary' : '🤖 Generate Summary'}
                          </button>
                          <a href={article.url} target="_blank" rel="noopener noreferrer" className="btn-read">
                            Read Full Article →
                          </a>
                        </div>
                        {summaries[article.id || index] && (
                          <div className="summary-container">
                            <div className="summary-header">
                              <span>✨ AI Summary {stats.ragEnabled && '(with RAG context)'}</span>
                            </div>
                            <p className="summary-text">{summaries[article.id || index]}</p>
                          </div>
                        )}
                      </div>
                    ))
                  ) : (
                    <div className="empty-state">
                      <div className="empty-icon">📭</div>
                      <h3>No articles found</h3>
                      <p>Try changing your search query or selecting a different category</p>
                      <button onClick={() => {
                        setSearchQuery('');
                        setSelectedCategory('all');
                        fetchNews('personalized');
                      }}>Reset Filters</button>
                    </div>
                  )}
                </div>
              )}
            </>
          )}

          {activeTab === 'stats' && (
            <div className="stats-container">
              <h2>📊 Your Reading Statistics</h2>
              <div className="stats-grid">
                <div className="stat-card">
                  <div className="stat-icon">📰</div>
                  <h3>Articles Read</h3>
                  <div className="stat-number">{stats.totalRead}</div>
                </div>
                <div className="stat-card">
                  <div className="stat-icon">🎯</div>
                  <h3>Active Interests</h3>
                  <div className="stat-number">{stats.interests?.length || 0}</div>
                  <div className="stat-detail">
                    {stats.interests?.slice(0, 4).join(', ')}
                    {stats.interests?.length > 4 && '...'}
                  </div>
                </div>
                <div className="stat-card">
                  <div className="stat-icon">🧠</div>
                  <h3>RAG Status</h3>
                  <div className={`stat-number ${stats.ragEnabled ? 'enabled' : 'disabled'}`}>
                    {stats.ragEnabled ? 'ACTIVE' : 'OFF'}
                  </div>
                  <div className="stat-detail">
                    {stats.ragEnabled ? 'Context-aware summaries' : 'Basic summaries'}
                  </div>
                </div>
                <div className="stat-card">
                  <div className="stat-icon">📬</div>
                  <h3>News Sources</h3>
                  <div className="stat-number">4</div>
                  <div className="stat-detail">NewsAPI, Guardian, NewsData.io, World News</div>
                </div>
              </div>
              
              <div className="tips-section">
                <h3>💡 Pro Tips</h3>
                <ul>
                  <li>Click on any category chip to filter news by topic</li>
                  <li>Use the search bar to find news on specific topics</li>
                  <li>Click "Generate Summary" for AI-powered analysis</li>
                  <li>Update your interests for personalized recommendations</li>
                  <li>RAG provides historical context for better summaries</li>
                </ul>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;