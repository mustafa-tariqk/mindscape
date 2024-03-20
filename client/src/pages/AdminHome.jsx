import Neuma from '../img/Logo_with_subtext_upscaled.png'
import KeyboardIcon from '../img/keyboard.png'
import GearIcon from '../img/gear.png'
import PeopleIcon from '../img/people.png'
import RobotIcon from '../img/robot.png'
import ShieldIcon from '../img/shield.png'
import StatisticsIcon from '../img/statistics.png'
import React, { useState } from 'react'
import Sidebar from '../components/sidebar.jsx'
import GridList from '../components/GridList.jsx'
import GridComponent from '../components/GridComponent.jsx'
import './AdminHome.scss'
import Topbar from '../components/Topbar.jsx'


const AdminHome = () => {
    return (
        <div className='adminhome'>
            <div className='sidebar'>
                <Sidebar />
            </div>
            <div className='gridcomponent'>
                <GridComponent />
            </div>
         
        </div>
    )
}

export default AdminHome;