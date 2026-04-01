import React from 'react';
import { FiHome, FiUser, FiBarChart2, FiSettings } from 'react-icons/fi';
import './Sidebar.css';

function Sidebar({ activeTab, setActiveTab }) {
  const menuItems = [
    { id: 'feed', label: 'News Feed', icon: FiHome },
    { id: 'preferences', label: 'Preferences', icon: FiSettings },
    { id: 'stats', label: 'Statistics', icon: FiBarChart2 },
  ];

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h2>📬 NewsFlow</h2>
      </div>
      <nav className="sidebar-nav">
        {menuItems.map(item => (
          <div
            key={item.id}
            className={`nav-item ${activeTab === item.id ? 'active' : ''}`}
            onClick={() => setActiveTab(item.id)}
          >
            <item.icon className="nav-icon" />
            <span>{item.label}</span>
          </div>
        ))}
      </nav>
    </div>
  );
}

export default Sidebar;