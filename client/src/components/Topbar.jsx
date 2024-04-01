import React, { useState } from 'react';
import image1 from '../img/Logo_with_subtext_upscaled.png';
import image2 from '../img/userprofile.png';

const SERVER_URL = process.env.SERVER_URL;

const Topbar = () => {
    const [isDropdownOpen, setIsDropdownOpen] = useState(false);

    const toggleDropdown = () => {
        setIsDropdownOpen(!isDropdownOpen);
    };

    const handleLogout = () => {
        window.location.href = SERVER_URL + '/logout';
    }

    const handleLogin = () => {
        window.location.href = SERVER_URL + '/login';
    }

    return (
        <div className="topbar">
            <div className="left">
                <img src={image1} alt="Image 1" />
            </div>
            <div className="right">
                <div className="dropdown">
                    <img src={image2} alt="User Profile" onClick={toggleDropdown} style={{cursor: 'pointer'}} />
                    {isDropdownOpen && (
                        <div className="dropdown-content">
                            <div className='logout'>
                                <button onClick={handleLogout}>Logout</button>
                            </div>

                            <div className='login'>
                                <button onClick={handleLogin}>Login</button>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default Topbar;
