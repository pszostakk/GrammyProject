import React from 'react';
import Navbar from '../Navbar/Navbar';
import SearchTab from '../SearchTab/SearchTab';
import './Layout.css';

const Layout = ({ children }) => {
  return (
    <div className="app-layout">
      <Navbar />
      <div className="layout-right">
        <SearchTab />
        <div className="layout-content">
          {children}
        </div>
      </div>
    </div>
  );
};

export default Layout;