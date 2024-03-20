import Neuma from '../img/Logo_with_subtext_upscaled.png'
import KeyboardIcon from '../img/keyboard.png'
import GearIcon from '../img/gear.png'
import PeopleIcon from '../img/people.png'
import RobotIcon from '../img/robot.png'
import ShieldIcon from '../img/shield.png'
import StatisticsIcon from '../img/statistics.png'
import React, { useState } from 'react'


const Sidebar = () => {
    return (
        <div className='adminhome'>
            <div className="sidebar">
                <div className="logoBox">
                    <img src={Neuma} alt="Image 1" className="item-image" />
                </div>
                <div className="item">
                    <img src={KeyboardIcon} alt="Image 1" className="item-image" />
                    <span className="item-text">Submissions</span>
                </div>
                <div className="item">
                    <img src={PeopleIcon} alt="Image 1" className="item-image" />
                    <span className="item-text">Users</span>
                </div>
                <div className="item">
                    <img src={StatisticsIcon} alt="Image 1" className="item-image" />
                    <span className="item-text">Analytics</span>
                </div>
                <div className="item">
                    <img src={RobotIcon} alt="Image 1" className="item-image" />
                    <span className="item-text">Chatbot Management</span>
                </div>
                <div className="item">
                    <img src={GearIcon} alt="Image 1" className="item-image" />
                    <span className="item-text">Settings</span>
                </div>
                <div className="item">
                    <img src={ShieldIcon} alt="Image 1" className="item-image" />
                    <span className="item-text">FAQ</span>
                </div>
            </div>
            <div className='infoSide'>
            </div>
        </div>
    )
}

export default Sidebar;