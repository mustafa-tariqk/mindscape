import React, { useState } from 'react'
import ChangePermission from '../components/ChangePermission.jsx';
import ChatAction from '../components/ChatAction.jsx';


const AdminUsers = () => {
    const [selectedUser, setSelectedUser] = useState(null);

    return (
        <div className="admin-users">
        <h2>Change User Permissions</h2>
         <ChangePermission />
        {/* <h2>Chat Actions</h2>
        <ChatAction /> */}
        </div>
    );
}

export default AdminUsers;