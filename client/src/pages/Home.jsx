import React, { useState } from 'react'
import Chat from '../components/Chat.jsx'
import Topbar from '../components/Topbar.jsx'
import {
	BrowserRouter as Router,
	Routes,
	Route,
	Link
} from 'react-router-dom'
import Complete from './Complete.jsx';

function Home() {

    //Chat id passing
    const [chatId, setChatId] = useState(null);

    return (
        <div className='home'>
            <div className='topbar'>
                <Topbar/>
            </div>
            <Router>
                <div className='container'>
                    <Routes>
                        <Route path="/" element={<Chat chatId={chatId} setChatId={setChatId}/>} />
                        <Route path="/complete" element={<Complete chatId={chatId} />} />
                        <Route path="/logout" element={<handleLogout />} />
                    </Routes>
                </div>
            </Router>
        </div>
    )
}

export default Home