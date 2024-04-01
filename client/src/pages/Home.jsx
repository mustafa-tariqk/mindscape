import React, { useState } from 'react'
import {
    BrowserRouter as Router,
    Routes,
    Route,
} from 'react-router-dom'

import Complete from './Complete.jsx';
import Chat from '../components/Chat.jsx'
import Topbar from '../components/Topbar.jsx'
import Login from './Login.jsx'


function Home() {

    //Chat id passing
    const [chatId, setChatId] = useState(null);
    const [userId, setUserId] = useState(null);

    return (
        <Router>
            <div className='home'>
                <div className='topbar'>
                    <Topbar />
                </div>
                <div className='container'>
                    <Routes>
                        <Route path="/" element={<Chat chatId={chatId} userId={userId} setChatId={setChatId} setUserId={setUserId}/>}/>
                        <Route path="/complete" element={<Complete chatId={chatId} />} />
                        <Route path="/login" element={<Login />} />
                        <Route path="/logout" element={<handleLogout />} />
                    </Routes>
                </div>
            </div>
        </Router>
    )
}

export default Home