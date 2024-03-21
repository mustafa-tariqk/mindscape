import React from 'react';
const gridData = [
    {
      email: 'adminemail@gmail.com',
      name: 'Admi Ntester',
      role: 'Admin',
      startDate: '12.3.1987',
      endDate: '12.1.2023',
    },
    // ... You can add more user data here
  ];
  
  const GridComponent = () => {
    return (
      <div style={{ display: 'flex', flexDirection: 'column' }}>
        {gridData.map((user, index) => (
          <div key={index} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '10px', borderBottom: '1px solid #ccc' }}>
            <input type="checkbox" />
            <span style={{ flex: 2 }}>{user.email}</span>
            <span style={{ flex: 2 }}>{user.name}</span>
            <span style={{ flex: 1 }}>{user.role}</span>
            <span style={{ flex: 1 }}>{user.startDate}</span>
            <span style={{ flex: 1 }}>{user.endDate}</span>
            <span>•••</span>
          </div>
        ))}
      </div>
    );
  };
  
  export default GridComponent;