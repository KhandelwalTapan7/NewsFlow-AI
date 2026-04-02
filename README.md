
## ✨ Features

### 🤖 AI-Powered Intelligence
- **BART Transformer Model**: Generates concise, human-like summaries of news articles
- **RAG (Retrieval-Augmented Generation)**: Retrieves historical context for deeper, more meaningful insights
- **Smart Categorization**: Automatically classifies news into 7+ topics with high accuracy

### 📡 Multi-Source News Aggregation
| Source | Coverage | Features |
|--------|----------|----------|
| **NewsAPI** | Global headlines | 100+ countries, real-time updates |
| **The Guardian** | Quality journalism | In-depth analysis, trusted sources |
| **NewsData.io** | Breaking news | Real-time alerts, 24/7 coverage |
| **World News API** | International news | 50+ languages, global perspective |

### 🎯 Personalization
- **Interest-Based Filtering**: Select topics you care about (Tech, Sports, Business, etc.)
- **Personalized Feed**: News tailored to your unique preferences
- **Reading Statistics**: Track your reading habits and discover patterns
- **Category Filters**: 7+ categories with visual indicators

### 🎨 Modern User Experience
- **Glassmorphism Design**: Beautiful gradient backgrounds with blur effects
- **Floating Particles**: Dynamic animated background for visual appeal
- **Fully Responsive**: Seamless experience across desktop, tablet, and mobile
- **Smooth Animations**: Fluid transitions and hover effects
- **Dark/Light Mode**: Automatic theme detection

### 🔐 Complete User Management
- **JWT Authentication**: Secure login and session management
- **User Profiles**: Save preferences, interests, and reading history
- **Onboarding Tutorial**: Guided introduction for new users
- **Reading History**: Track articles you've already read

## 🚀 Quick Start

### Prerequisites

| Requirement | Version | Download |
|-------------|---------|----------|
| Python | 3.9+ | [python.org](https://www.python.org/downloads/) |
| Node.js | 16+ | [nodejs.org](https://nodejs.org/) |
| Git | Latest | [git-scm.com](https://git-scm.com/) |
| RAM | 4GB+ | For AI model inference |
| Storage | 5GB+ | For AI model files (optional) |

### API Keys Required

Get free API keys from these providers:

1. **[NewsAPI](https://newsapi.org/register)** - 100 requests/day free
2. **[The Guardian](https://open-platform.theguardian.com/access/)** - Free tier available
3. **[NewsData.io](https://newsdata.io/register)** - 200 requests/day free
4. **[World News API](https://worldnewsapi.com/register)** - Free tier available

### Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/KhandelwalTapan7/NewsFlow-AI.git
cd NewsFlow-AI
```

#### 2. Backend Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

#### 3. Frontend Setup
```bash
cd frontend
npm install
cd ..
```

#### 4. Environment Configuration
```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your API keys
# Windows:
notepad .env
# Mac/Linux:
nano .env
```

#### 5. Run the Application

**Terminal 1 - Backend Server:**
```bash
python api.py
```

**Terminal 2 - Frontend Development Server:**
```bash
cd frontend
npm start
```

**Open your browser:** http://localhost:3000

## 📁 Project Structure

```
NewsFlow-AI/
│
├── api.py                          # FastAPI backend server
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore rules
├── README.md                       # Project documentation
├── LICENSE                         # MIT License
│
├── src/                            # Backend source code
│   ├── __init__.py
│   ├── news_fetcher.py            # News API integration (4 sources)
│   ├── summarizer.py              # AI summarization & RAG logic
│   ├── user_profiles.py           # User management & preferences
│   ├── notifier.py                # Notification system
│   │
│   ├── config/                    # Configuration files
│   │   ├── __init__.py
│   │   └── settings.py            # Application settings
│   │
│   └── utils/                     # Utility functions
│       ├── __init__.py
│       ├── helpers.py             # Helper functions
│       ├── logger.py              # Logging configuration
│       └── validators.py          # Input validation
│
└── frontend/                      # React frontend
    ├── public/
    │   └── index.html             # HTML template
    ├── src/
    │   ├── App.js                 # Main React component
    │   ├── App.css                # Styling with animations
    │   ├── Auth.js                # Login/Signup component
    │   ├── Onboarding.js          # Tutorial component
    │   ├── index.js               # Entry point
    │   └── index.css              # Global styles
    └── package.json               # Frontend dependencies
```

## 🎯 Features in Detail

### 📰 News Feed
- **Category Chips**: Click any category (Sports, Technology, etc.) for instant filtering
- **Search Bar**: Find specific topics across all 4 news sources
- **Source Filter**: Filter by individual news sources
- **Sort Options**: Latest first or oldest first
- **View Toggle**: Grid view or list view
- **Real-time Updates**: Auto-refresh with latest news

### 🤖 AI Summaries
- **One-Click Summarization**: Generate AI summary for any article
- **RAG Context**: Automatically adds historical context when available
- **Smart Categorization**: AI detects article category automatically
- **Toggle Visibility**: Show or hide summaries on demand
- **Reading Time**: Estimated reading time for each article

### 📊 Statistics Dashboard
- **Articles Read**: Track your reading progress
- **Active Interests**: See your selected topics at a glance
- **RAG Status**: Context-aware summaries indicator
- **News Sources**: Active sources and their status
- **Reading Trends**: Visual insights into your habits

### 👤 User Profile
- **Personalized Greeting**: Time-based welcome message (Good Morning, etc.)
- **Interest Management**: Update preferences anytime
- **Reading History**: Track articles you've already seen
- **Secure Logout**: One-click session termination

## 🛠️ Technology Stack

### Backend
| Technology | Purpose | Version |
|------------|---------|---------|
| **FastAPI** | Web framework | 0.104+ |
| **Transformers** | AI models (BART) | 4.36+ |
| **PyTorch** | Deep learning | 2.1+ |
| **JWT** | Authentication | 2.8+ |
| **Redis** | Caching (optional) | 5.0+ |
| **Python-dotenv** | Environment config | 1.0+ |

### Frontend
| Technology | Purpose | Version |
|------------|---------|---------|
| **React** | UI framework | 18.2+ |
| **Axios** | HTTP client | 1.6+ |
| **React Hot Toast** | Notifications | 2.4+ |
| **CSS3** | Animations & styling | - |

### AI Models
| Model | Size | Purpose |
|-------|------|---------|
| **DistilBART-CNN-12-6** | 1.2GB | Summarization (default) |
| **BART-Large-CNN** | 1.6GB | Higher quality summaries |

## 🔧 Configuration

### Environment Variables (.env)

```env
# ============================================
# API KEYS (Required)
# ============================================
NEWS_API_KEY=your_newsapi_key_here
GUARDIAN_API_KEY=your_guardian_key_here
NEWSDATA_IO_API_KEY=your_newsdata_io_key_here
WORLD_NEWS_API_KEY=your_world_news_key_here

# ============================================
# REDIS CONFIGURATION (Optional)
# ============================================
REDIS_URL=redis://localhost:6379

# ============================================
# MODEL CONFIGURATION
# ============================================
SUMMARIZATION_MODEL=sshleifer/distilbart-cnn-12-6
USE_GPU=false
BATCH_SIZE=4
MODEL_CACHE_DIR=./models/cache

# ============================================
# APPLICATION SETTINGS
# ============================================
DEBUG=true
ENVIRONMENT=development
SECRET_KEY=your-secret-key-change-in-production
RAG_ENABLED=true
MAX_ARTICLES_PER_FETCH=50
DEFAULT_COUNTRY=us
```

### Production Checklist

- [ ] Set `DEBUG=false` in `.env`
- [ ] Use PostgreSQL instead of JSON files
- [ ] Configure proper CORS origins
- [ ] Set up SSL/TLS certificates
- [ ] Use environment-specific API keys
- [ ] Enable Redis caching
- [ ] Set up monitoring and logging
- [ ] Configure backup strategy

## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| **Summary Generation** | 2-5 seconds per article |
| **News Fetch Time** | 3-8 seconds (4 sources) |
| **Page Load Time** | < 2 seconds |
| **Concurrent Users** | 50+ supported |
| **Daily Article Limit** | 200+ (free tier) |

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add AmazingFeature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 for Python code
- Use ESLint for JavaScript/React
- Write meaningful commit messages
- Add comments for complex logic
- Update documentation when needed

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Hugging Face** - For Transformers library and BART model
- **Facebook AI** - For BART architecture
- **FastAPI** - For excellent Python framework
- **React** - For frontend library
- **All News API Providers** - For making news data accessible

## 📞 Contact & Support

**Author:** Tapan Khandelwal
- GitHub: [@KhandelwalTapan7](https://github.com/KhandelwalTapan7)
- Project Link: [NewsFlow-AI](https://github.com/KhandelwalTapan7/NewsFlow-AI)

**Issues:** [Report a bug](https://github.com/KhandelwalTapan7/NewsFlow-AI/issues)

