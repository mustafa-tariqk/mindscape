import React, { useState } from 'react';
import image1 from '../img/Logo_with_subtext_upscaled.png';
import image2 from '../img/userprofile.png';
import { useNavigate } from 'react-router-dom'; // Make sure to import useNavigate

const SERVER_URL = process.env.SERVER_URL;

const Topbar = () => {
    const [isDropdownOpen, setIsDropdownOpen] = useState(false);
    const navigate = useNavigate(); // Use the useNavigate hook

    const toggleDropdown = () => {
        setIsDropdownOpen(!isDropdownOpen);
    };

  
    const handleLogout = () => {
        // Instead of manipulating the DOM, use navigate to change the route
      navigate(SERVER_URL + '/logout'); // Assuming '/logout' is a route that handles your logout logic
      console.log("Logging out");
    };

    return (
        <div className="topbar">
            <div className="left">
                <img src={image1} alt="Image 1" />
            </div>
            <div className="gap"></div>
            <div className="right">
                <a href="#">Explore Experiences</a>
                <a href="#">FAQ</a>
                <div className="dropdown">
                    <img src={image2} alt="User Profile" onClick={toggleDropdown} style={{cursor: 'pointer'}} />
                    {isDropdownOpen && (
                        <div className="dropdown-content">
                            <button onClick={handleLogout}>Logout</button>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default Topbar;
