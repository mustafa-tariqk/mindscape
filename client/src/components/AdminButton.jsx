import React from 'react';
import { useNavigate } from "react-router-dom"
import AdminHome from '../pages/AdminHome.jsx';



const AdminButton = () => {
    const navigate = useNavigate()

    const handleSubmit = () => {
        navigate("/admin")
    }
    return (
        <div>
            <button onClick={handleSubmit}>Admin</button>
        </div>
    )
};

export default AdminButton;