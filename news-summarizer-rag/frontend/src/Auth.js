import React, { useState } from 'react';
import axios from 'axios';
import { toast } from 'react-hot-toast';
import './Auth.css';

const API_BASE_URL = 'http://localhost:8000';

function Auth({ onLogin }) {
  const [isLogin, setIsLogin] = useState(true);
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [selectedInterests, setSelectedInterests] = useState([]);
  const [errors, setErrors] = useState({});

  const availableInterests = [
    { id: 'technology', name: 'Technology', icon: '💻', color: '#4caf50' },
    { id: 'politics', name: 'Politics', icon: '🏛️', color: '#f39c12' },
    { id: 'business', name: 'Business', icon: '📊', color: '#2ecc71' },
    { id: 'health', name: 'Health', icon: '🏥', color: '#e74c3c' },
    { id: 'sports', name: 'Sports', icon: '⚽', color: '#3498db' },
    { id: 'science', name: 'Science', icon: '🔬', color: '#9b59b6' },
    { id: 'entertainment', name: 'Entertainment', icon: '🎬', color: '#e84393' }
  ];

  const validateForm = () => {
    const newErrors = {};
    
    if (!isLogin && !formData.name.trim()) {
      newErrors.name = 'Name is required';
    }
    
    if (!formData.email.trim()) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email is invalid';
    }
    
    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters';
    }
    
    if (!isLogin && formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }
    
    setLoading(true);
    
    try {
      if (isLogin) {
        // Login
        const response = await axios.post(`${API_BASE_URL}/api/v1/auth/login`, {
          email: formData.email,
          password: formData.password
        });
        
        if (response.data.success) {
          localStorage.setItem('token', response.data.token);
          localStorage.setItem('user', JSON.stringify(response.data.user));
          toast.success('Welcome back!');
          onLogin(response.data.user);
        } else {
          toast.error(response.data.error || 'Login failed');
        }
      } else {
        // Signup
        const response = await axios.post(`${API_BASE_URL}/api/v1/auth/signup`, {
          name: formData.name,
          email: formData.email,
          password: formData.password,
          interests: selectedInterests
        });
        
        if (response.data.success) {
          localStorage.setItem('token', response.data.token);
          localStorage.setItem('user', JSON.stringify(response.data.user));
          toast.success('Account created successfully!');
          onLogin(response.data.user);
        } else {
          toast.error(response.data.error || 'Signup failed');
        }
      }
    } catch (error) {
      console.error('Auth error:', error);
      toast.error(error.response?.data?.error || 'Authentication failed');
    } finally {
      setLoading(false);
    }
  };

  const toggleInterest = (interestId) => {
    if (selectedInterests.includes(interestId)) {
      setSelectedInterests(selectedInterests.filter(i => i !== interestId));
    } else {
      if (selectedInterests.length < 5) {
        setSelectedInterests([...selectedInterests, interestId]);
      } else {
        toast.error('You can select up to 5 interests');
      }
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-header">
          <div className="auth-logo">📬</div>
          <h2>{isLogin ? 'Welcome Back!' : 'Create Account'}</h2>
          <p>{isLogin ? 'Sign in to continue' : 'Start your personalized news journey'}</p>
        </div>
        
        <form onSubmit={handleSubmit} className="auth-form">
          {!isLogin && (
            <div className="form-group">
              <label>Full Name</label>
              <input
                type="text"
                placeholder="Enter your name"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                className={errors.name ? 'error' : ''}
              />
              {errors.name && <span className="error-message">{errors.name}</span>}
            </div>
          )}
          
          <div className="form-group">
            <label>Email Address</label>
            <input
              type="email"
              placeholder="Enter your email"
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              className={errors.email ? 'error' : ''}
            />
            {errors.email && <span className="error-message">{errors.email}</span>}
          </div>
          
          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              placeholder="Enter your password"
              value={formData.password}
              onChange={(e) => setFormData({ ...formData, password: e.target.value })}
              className={errors.password ? 'error' : ''}
            />
            {errors.password && <span className="error-message">{errors.password}</span>}
          </div>
          
          {!isLogin && (
            <>
              <div className="form-group">
                <label>Confirm Password</label>
                <input
                  type="password"
                  placeholder="Confirm your password"
                  value={formData.confirmPassword}
                  onChange={(e) => setFormData({ ...formData, confirmPassword: e.target.value })}
                  className={errors.confirmPassword ? 'error' : ''}
                />
                {errors.confirmPassword && <span className="error-message">{errors.confirmPassword}</span>}
              </div>
              
              <div className="interests-section">
                <h3>Select Your Interests (Optional)</h3>
                <div className="interests-grid">
                  {availableInterests.map(interest => (
                    <div
                      key={interest.id}
                      className={`interest-tag ${selectedInterests.includes(interest.id) ? 'selected' : ''}`}
                      onClick={() => toggleInterest(interest.id)}
                    >
                      {interest.icon} {interest.name}
                    </div>
                  ))}
                </div>
                <p style={{ fontSize: '12px', color: '#999', marginTop: '8px' }}>
                  Select up to 5 interests for personalized news
                </p>
              </div>
            </>
          )}
          
          <button type="submit" className="auth-button" disabled={loading}>
            {loading ? 'Please wait...' : (isLogin ? 'Sign In' : 'Create Account')}
          </button>
        </form>
        
        <div className="auth-footer">
          {isLogin ? "Don't have an account? " : "Already have an account? "}
          <span onClick={() => {
            setIsLogin(!isLogin);
            setErrors({});
            setFormData({ name: '', email: '', password: '', confirmPassword: '' });
            setSelectedInterests([]);
          }}>
            {isLogin ? 'Sign Up' : 'Sign In'}
          </span>
        </div>
      </div>
    </div>
  );
}

export default Auth;