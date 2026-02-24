import React from 'react';
import Navbar from '../../components/Navbar/Navbar';
import SearchTab from '../../components/SearchTab/SearchTab';
import './HomePage.css';

const HomePage = () => {
  return (
    <div className="home-page">
      {/* Search Tab - Full Width */}
      <SearchTab />

      {/* Bottom Section - Navbar + Content */}
      <div className="bottom-section">
        <Navbar />
        <div className="page-content">
          <div className="empty-state">
            <h2>You have no projects yet!</h2>
            <p>Let's create one to get started</p>
            <button className="create-btn">Create +</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
