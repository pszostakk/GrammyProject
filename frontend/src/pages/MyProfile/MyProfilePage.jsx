import React, { useState, useEffect } from 'react';
import Layout from '../../components/Layout/Layout';
import './MyProfilePage.css';

const MyProfilePage = () => {
  // Stan komponentu
  const [displayName, setDisplayName] = useState('');
  const [newDisplayName, setNewDisplayName] = useState('');
  const [loading, setLoading] = useState(true);

  // Pobranie aktualnego displayName z Cognito przy ładowaniu strony
  useEffect(() => {
    const fetchUser = async () => {
      try {
        const user = await Auth.currentAuthenticatedUser();
        const currentName = user.attributes['custom:displayName'] || '';
        setDisplayName(currentName);
        setNewDisplayName(currentName);
      } catch (error) {
        console.error('Error fetching user:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, []);

  // Funkcja zapisu nowego displayName
  const handleSave = async () => {
    try {
      const user = await Auth.currentAuthenticatedUser();
      await Auth.updateUserAttributes(user, {
        'custom:displayName': newDisplayName,
      });
      setDisplayName(newDisplayName);
      alert('Display name updated successfully!');
    } catch (error) {
      console.error('Error updating display name:', error);
      alert('Failed to update display name.');
    }
  };

  if (loading) return <p>Loading profile...</p>;

  return (
    <Layout>
      <div className="profile-container">
        <h2>Profile Settings</h2>

        <div className="profile-card">
          <label htmlFor="displayName">Display Name</label>
          <input
            id="displayName"
            type="text"
            value={newDisplayName}
            onChange={(e) => setNewDisplayName(e.target.value)}
          />
          <button onClick={handleSave}>Save Changes</button>
        </div>

        <div className="profile-preview">
          <p>
            <strong>Current Display Name:</strong> {displayName || '(not set)'}
          </p>
        </div>
      </div>
    </Layout>
  );
};

export default MyProfilePage;