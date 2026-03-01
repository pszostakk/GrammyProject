import React, { useState } from 'react';
import './Navbar.css';

const Navbar = () => {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [accountMenuOpen, setAccountMenuOpen] = useState(false);

  const toggleSidebar = () => {
    setIsCollapsed(!isCollapsed);
  };

  const toggleAccountMenu = () => {
    setAccountMenuOpen(!accountMenuOpen);
  };

  const navItems = [
    { id: 1, label: 'Home', icon: '🏠' },
    { id: 2, label: 'Projects', icon: '📁' },
    { id: 3, label: 'Instruments', icon: '🎸' },
    { id: 4, label: 'Songs', icon: '🎵' },
    { id: 5, label: 'Tunings', icon: '🎼' },
    { id: 6, label: 'Settings', icon: '⚙️' },
    { id: 7, label: 'Help', icon: '❓' },
  ];

  return (
    <aside className={`navbar ${isCollapsed ? 'collapsed' : ''}`}>
      {/* Toggle Button */}
      <button className="toggle-btn" onClick={toggleSidebar} title="Toggle Sidebar">
        {isCollapsed ? '→' : '←'}
      </button>

      {/* Navigation Items */}
      <nav className="nav-menu">
        {navItems.map((item) => (
          <button
            key={item.id}
            className="nav-item"
            title={item.label}
            onClick={() => {
              // TODO: Add navigation logic
              console.log(`Clicked: ${item.label}`);
            }}
          >
            <span className="nav-icon">{item.icon}</span>
            {!isCollapsed && <span className="nav-label">{item.label}</span>}
          </button>
        ))}
      </nav>

      {/* Bottom Section - Account Details */}
      <div className="navbar-bottom">
        <button
          className="account-btn"
          onClick={toggleAccountMenu}
          title="Account Details"
        >
          <span className="nav-icon">👤</span>
          {!isCollapsed && (
            <>
              <span className="nav-label">Account</span>
              <span className="account-arrow">{accountMenuOpen ? '▲' : '▼'}</span>
            </>
          )}
        </button>
        
        {accountMenuOpen && (
          <div className="account-menu">
            <button
              className="logout-btn"
              onClick={() => {
                // TODO: Add logout logic
                console.log('Logout clicked');
              }}
            >
              <span className="nav-icon">🚪</span>
              {!isCollapsed && <span className="nav-label">Logout</span>}
            </button>
          </div>
        )}
      </div>
    </aside>
  );
};

export default Navbar;
