import React, { useState } from 'react';

const SERVER_URL = process.env.SERVER_URL;

const ChatAction = () => {
  const [chatId, setChatId] = useState('');
  const [action, setAction] = useState('delete'); // 'delete' or 'flag'
  const [showForm, setShowForm] = useState(false); // State to control the visibility of the form

  const handleChatIdChange = (e) => {
    setChatId(e.target.value);
  };

  const handleActionChange = (e) => {
    setAction(e.target.value);
  };

  const toggleFormVisibility = () => {
    setShowForm(!showForm);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const endpoint = action === 'delete'
      ? `/api/delete_chat/${chatId}`
      : `/api/flag/${chatId}`;

    try {
      const response = await fetch(SERVER_URL + endpoint, {
        method: 'GET', // Adjust if your API uses a different method
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
      alert(`Chat ${action}d successfully!`);
    } catch (error) {
      // Handle errors
      console.error(`Error ${action}ing chat:`, error);
      alert(`Failed to ${action} chat.`);
    }
  };

  return (
    <div className="chat-action-container">
      <button onClick={toggleFormVisibility} className="toggle-form-button">
        {showForm ? 'Hide Chat Action Form' : 'Show Chat Action Form'}
      </button>
      {showForm && (
        <form onSubmit={handleSubmit} className={showForm ? 'show' : ''}>
          <label htmlFor="chatId">Chat ID:</label>
          <input
            type="text"
            id="chatId"
            value={chatId}
            onChange={handleChatIdChange}
            required
          />

          <label htmlFor="action">Action:</label>
          <select id="action" value={action} onChange={handleActionChange} required>
            <option value="delete">Delete</option>
            <option value="flag">Flag</option>
          </select>

          <button type="submit">{action === 'delete' ? 'Delete Chat' : 'Flag Chat'}</button>
        </form>
      )}
    </div>
  );
};

export default ChatAction;
