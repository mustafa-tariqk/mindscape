import React, { useState } from 'react';

const SERVER_URL = process.env.SERVER_URL;

const ChangePermission = () => {
  const [email, setEmail] = useState('');
  const [role, setRole] = useState('Administrator');

  const handleChangeEmail = (e) => {
    setEmail(e.target.value);
  };

  const handleChangeRole = (e) => {
    setRole(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevents the default form submit action

    try {
      // Assuming you're using fetch for HTTP requests
      const response = await fetch(SERVER_URL + `/api/change_permission/${email}/${role}`, {
          method: 'GET', // or 'PUT', depending on your backend implementation
          mode: 'cors',
          credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
          // Include other headers as required by your backend
        },
        // If your API expects a request body, include it here
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

  return (
    <div>
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
    </div>
  );
};

export default ChangePermission;
