import React from 'react';
import Layout from '../../components/Layout/Layout';
import './HomePage.css';

const HomePage = () => {
  return (
    <Layout>
      <div className="page-content">
        <div className="empty-state">
          <h2>You have no projects yet!</h2>
          <p>Let's create one to get started</p>
          <button className="create-btn">Create +</button>
        </div>
      </div>
    </Layout>
  );
};

export default HomePage;