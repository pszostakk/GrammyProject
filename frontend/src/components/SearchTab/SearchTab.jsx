import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './SearchTab.css';

const SearchTab = () => {
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState('');
  const [showNotifications, setShowNotifications] = useState(false);

  const handleLogoClick = () => {
    navigate('/');
  };

  const handleAvatarClick = () => {
    navigate('/myProfile');
  };

  const handleNotificationClick = () => {
    setShowNotifications(!showNotifications);
  };

  const handleSearchChange = (e) => {
    setSearchQuery(e.target.value);
  };

  return (
    <div className="search-tab">
      {/* Top row: Logo, Search, Notification, Avatar */}
      <div className="search-tab-header">
        {/* Logo */}
        <div className="logo-container">
          <img
            src="/logo.png"
            alt="Logo"
            className="logo"
            onClick={handleLogoClick}
          />
        </div>

        {/* Search Bar */}
        <div className="search-bar-container">
          <input
            type="text"
            className="search-bar"
            placeholder="Search..."
            value={searchQuery}
            onChange={handleSearchChange}
          />
        </div>

        {/* Notification Icon */}
        <div className="notification-container">
          <button
            className="notification-btn"
            onClick={handleNotificationClick}
            title="Notifications"
          >
            🔔
          </button>
          {showNotifications && (
            <div className="notifications-window">
              <div className="notifications-header">
                <h3>Notifications</h3>
                <button
                  className="close-btn"
                  onClick={() => setShowNotifications(false)}
                >
                  ✕
                </button>
              </div>
              <div className="notifications-content">
                <p>No notifications yet</p>
              </div>
            </div>
          )}
        </div>

        {/* Avatar Icon */}
        <div className="avatar-container">
          <button
            className="avatar-btn"
            onClick={handleAvatarClick}
            title="My Profile"
          >
            👤
          </button>
        </div>
      </div>

      {/* Bottom row: Four action buttons */}
      <div className="search-tab-actions">
        <button className="action-btn">Button 1</button>
        <button className="action-btn">Button 2</button>
        <button className="action-btn">Button 3</button>
        <button className="action-btn">Button 4</button>
      </div>
    </div>
  );
};

export default SearchTab;
