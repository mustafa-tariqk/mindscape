import React, { useState } from 'react'
import Topbar from '../components/Topbar.jsx'
import TrollsList from '../components/TrollsList.jsx'
import ChangePermission from '../components/ChangePermission.jsx'
import ChatAction from '../components/ChatAction.jsx'


const AdminHome = () => {
    // const [results, setResults] = useState([]);

    return (
        <div className='adminhome'>
            <Topbar />
            <div className='trollslist'>
                <TrollsList />
            </div>    
            <div className='changepermission'>
                <ChangePermission />
            </div>
            <div className='chataction'>
                <ChatAction />
            </div>

         
        </div>
    )
}

export default AdminHome;