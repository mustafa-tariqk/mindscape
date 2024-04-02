import React, { useState } from 'react';

const SERVER_URL = process.env.SERVER_URL;

const ChangePermission = () => {
  const [email, setEmail] = useState('');
  const [role, setRole] = useState('Administrator');
  const [showForm, setShowForm] = useState(false); // State to control the visibility of the form

  const handleChangeEmail = (e) => {
    setEmail(e.target.value);
  };

  const handleChangeRole = (e) => {
    setRole(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevents the default form submission action

    // URL construction with encodeURIComponent to ensure special characters are properly encoded
    const url = `/api/change_permission/${encodeURIComponent(email)}/${encodeURIComponent(role)}`;

    try {
      const response = await fetch(SERVER_URL + url, {
        method: 'GET', // or 'POST' if your implementation changes
        mode: 'cors',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      // Handle success
      alert('Permission changed successfully!');
    } catch (error) {
      // Handle errors
      console.error('Error changing permission:', error);
      alert('Failed to change permission.');
    }
  };

  const toggleForm = () => {
    setShowForm(!showForm);
  };

  return (
    <div className="change-permission">
      <button onClick={toggleForm} className="toggle-form-button">
        {showForm ? 'Hide Change Permission Form' : 'Show Change Permission Form'}
      </button>
      {showForm && (
        <form onSubmit={handleSubmit}>
          <label htmlFor="email">User Email:</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={handleChangeEmail}
            required
          />

          <label htmlFor="role">Role:</label>
          <select id="role" value={role} onChange={handleChangeRole} required>
            <option value="Administrator">Administrator</option>
            <option value="Researcher">Researcher</option>
            <option value="Contributor">Contributor</option>
          </select>

          <button type="submit">Change Permission</button>
        </form>
      )}
    </div>
  );
};

export default ChangePermission;
