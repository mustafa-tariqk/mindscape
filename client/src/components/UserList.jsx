import React, { useState, useEffect } from 'react';
import axios from 'axios';

const SERVER_URL = process.env.SERVER_URL;

const UserList = () => {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await axios.get(SERVER_URL + '/api/get_trolls');
        setUsers(response.data);
        console.log('Users:', response.data);
      } catch (error) {
        console.error('Error fetching users:', error);
      }
    };

    fetchUsers();
  }, []);

  return (
    <div>
      <h2>Users List</h2>
      <div>
      <p>Email: {users.email}</p>
      <p>Role: {users.role}</p>
      <p>User ID: {users.user_id}</p>
    </div>
    </div>
  );
}

export default UserList;
