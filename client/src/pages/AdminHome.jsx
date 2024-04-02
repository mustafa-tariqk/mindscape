import React, { useState } from 'react'
import Topbar from '../components/Topbar.jsx'
import TrollsList from '../components/TrollsList.jsx'
import ChangePermission from '../components/ChangePermission.jsx'
import ChatAction from '../components/ChatAction.jsx'
import DownloadChatsButton from '../components/DownloadAllChats.jsx'


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
            <div>
                <DownloadChatsButton />
            </div>
            <div className='footer-text'>
                Want to become a researcher/administrator? Email <a href="mailto:neuma.mindscape@gmail.com">neuma.mindscape@gmail.com</a>
            </div>

         
        </div>
    )
}

export default AdminHome;