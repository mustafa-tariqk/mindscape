import React, { useState, useEffect } from 'react';
import image1 from '../img/Logo_with_subtext_upscaled.png';
import { useNavigate } from "react-router-dom"

const SERVER_URL = process.env.SERVER_URL;

const Topbar = () => {
    const [isLoggedIn, setIsLoggedIn] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        // You would replace this with a real check to your authentication system
        // For example, check if a token exists in local storage, or make an API call
        const checkLoginStatus = async () => {
            try {
                const response = await fetch(SERVER_URL + '/api/user', {
                    method: 'GET',
                    mode: 'cors',
                    credentials: 'include', // For sending cookies over cross-origin requests
                });
                const data = await response.json();
                setIsLoggedIn(true);
                console.log('Login status:', data);
            } catch (error) {
                console.error('Error checking login status:', error);
                setIsLoggedIn(false);
                console.log('Login status:', false);
            }
        };

        checkLoginStatus();
    }, []);

    const handleLogout = () => {
        window.location.href = SERVER_URL + '/logout';
    }

    const handleLogin = () => {
        window.location.href = SERVER_URL + '/login';
    }

    const handleAdmin = () => {
        navigate("/admin")
    }

    const handleHome = () => {
        navigate("/")
    }

    return (
        <div className="topbar">
            <div className="left">
                <img src={image1} alt="Neuma logo" onClick={handleHome}/>
            </div>
            <button onClick={handleAdmin} className='admin-button'>Admin/Researcher Window</button>
            <div className="right">
                {isLoggedIn ? (
                    <button onClick={handleLogout} className='logout-button'>Logout</button>
                ) : (
                    <button onClick={handleLogin} className='login-button'>Login</button>
                )}
            </div>
        </div>
    );
}

export default Topbar;
