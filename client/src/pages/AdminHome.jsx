import React, { useState } from 'react'
import GridList from '../components/GridList.jsx'
import UserList from '../components/UserList.jsx'
import './AdminHome.scss'
import Topbar from '../components/Topbar.jsx'
import TrollsList from '../components/TrollsList.jsx'


const AdminHome = () => {
    // const [results, setResults] = useState([]);

    return (
        <div className='adminhome'>
            <Topbar />
            <div className='trollslist'>
                <TrollsList />
            </div>
         
        </div>
    )
}

export default AdminHome;