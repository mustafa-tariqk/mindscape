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
            <Router>
                <div className='topbar'>
                    <Topbar/>
                </div>
                <div className='container'>
                    <Routes>
                        <Route path="/" element={<Chat chatId={chatId} setChatId={setChatId}/>} />
                        <Route path="/complete" element={<Complete chatId={chatId} />} />
                        {/* Make sure to update or remove the "/logout" route if it's intended to use a specific component or handler */}
                        <Route path="/logout" element={<handleLogout />} />
                    </Routes>
                </div>
                </Router>
            </div>
    )
}

export default Home;
