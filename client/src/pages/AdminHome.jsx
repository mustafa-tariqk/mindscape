import React, { useState } from 'react'
import Sidebar from '../components/Sidebar.jsx'
import GridList from '../components/GridList.jsx'
import UserList from '../components/UserList.jsx'
import './AdminHome.scss'
import Topbar from '../components/Topbar.jsx'
import TrollList from '../components/TrollsList.jsx'


const AdminHome = () => {
    // const [results, setResults] = useState([]);

    return (
        <div className='adminhome'>
            <Sidebar />
            {/* <div className='userlist'>
                <UserList />
            </div> */}
            <div className='trolllist'>
                <TrollList />
            </div>
         
        </div>
    )
}

export default AdminHome;