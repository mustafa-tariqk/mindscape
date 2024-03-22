import React, { useState } from 'react';
import image1 from '../img/Logo_with_subtext_upscaled.png';
import image2 from '../img/userprofile.png';
import YourComponentLogout from '../components/YourComponenentLogout.jsx';

const Topbar = () => {
    const [isDropdownOpen, setIsDropdownOpen] = useState(false);

    const toggleDropdown = () => {
        setIsDropdownOpen(!isDropdownOpen);
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
                            <div className='yourcomponentlogout'>
                            <YourComponentLogout/>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default Topbar;
