import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { logoutUser } from '../../auth/authService';
import './Navbar.css';

const Navbar = () => {
  const navigate = useNavigate();
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [accountMenuOpen, setAccountMenuOpen] = useState(false);

  const toggleSidebar = () => {
    setIsCollapsed(!isCollapsed);
  };

  const toggleAccountMenu = () => {
    setAccountMenuOpen(!accountMenuOpen);
  };

  const handleLogout = async () => {
    try {
      await logoutUser();
      navigate('/loginPage');
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  const navItems = [
    { id: 1, label: 'Home', icon: '🏠', path: '/' },
    { id: 2, label: 'Projects', icon: '📁', path: null },
    { id: 3, label: 'Instruments', icon: '🎸', path: null },
    { id: 4, label: 'Songs', icon: '🎵', path: null },
    { id: 5, label: 'Tunings', icon: '🎼', path: null },
    { id: 6, label: 'Settings', icon: '⚙️', path: null },
    { id: 7, label: 'Help', icon: '❓', path: null },
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
              if (item.path) {
                navigate(item.path);
              } else {
                console.log(`Clicked: ${item.label}`);
              }
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
              className="account-menu-item"
              onClick={() => {
                navigate('/myProfile');
                setAccountMenuOpen(false);
              }}>
              <span className="nav-icon">👤</span>
              {!isCollapsed && (
                <span className="nav-label">My profile</span>
              )}
            </button>
            <button
              className="logout-btn"
              onClick={handleLogout}>
              <span className="nav-icon">🚪</span>
              {!isCollapsed && (
                <span className="nav-label">Logout</span>
              )}
            </button>
          </div>
        )}
      </div>
    </aside>
  );
};

export default Navbar;