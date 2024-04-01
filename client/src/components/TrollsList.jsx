import React, { useState } from 'react';

const SERVER_URL = process.env.SERVER_URL;

function TrollList() {
  const [trolls, setTrolls] = useState([]);
  const [showTrolls, setShowTrolls] = useState(false); // State to control visibility of the trolls list

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
      setShowTrolls(true); // Show the trolls list after fetching
    })
    .catch(error => console.error('Error fetching trolls:', error));
  };

  const deleteUser = (userEmail) => {
      fetch(SERVER_URL + `/api/delete_user/${encodeURIComponent(userEmail)}`, {
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
      <button onClick={fetchTrolls}>Show Flagged Users</button>
      {showTrolls && (
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
      )}
    </div>
  );
}

export default TrollList;
