import React, { useState, useEffect } from 'react';

const SERVER_URL = process.env.SERVER_URL;

function TrollList() {
  const [trolls, setTrolls] = useState([]);

  useEffect(() => {
    fetchTrolls();
  }, []);

  const fetchTrolls = () => {
      fetch(SERVER_URL + '/api/get_trolls', {
          mode: 'cors',
          method: 'GET',
          credentials: 'include',
      // Include headers as necessary, for example, Authorization headers
    })
    .then(response => response.json())
    .then(data => {
      const trollsArray = Object.keys(data).map(email => ({
        email,
        flag_count: data[email],
      }));
      setTrolls(trollsArray);
    })
    .catch(error => console.error('Error fetching trolls:', error));
  };

  const deleteUser = (userEmail) => {
    // Replace 'http://example.com/api/delete_user/' with your actual endpoint
      fetch(SERVER_URL + `/api/delete_user/${(userEmail)}`, {
          mode: 'cors',
          method: 'GET',
          credentials: 'include',
      // Include headers as necessary, e.g., Authorization headers
    })
    .then(response => {
      if (response.ok) {
        // Optionally refetch the trolls list or remove the user from state
        fetchTrolls(); // Refetching the list after deletion
      } else {
        console.error('Failed to delete user');
      }
    })
    .catch(error => console.error('Error deleting user:', error));
  };

  return (
    <div>
      <h2>Flagged Users</h2>
      <ul>
        {trolls.map((troll, index) => (
          <li key={index}>
            Email: {troll.email}, Flags: {troll.flag_count}
            <button onClick={() => deleteUser(troll.email)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default TrollList;
