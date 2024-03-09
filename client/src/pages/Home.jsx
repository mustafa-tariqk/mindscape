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

const SERVER_URL = process.env.SERVER_URL;


function Home() {

    //Login check here
    fetch(SERVER_URL+'/api/user', {
        method: 'GET',
        mode: 'cors',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if("error" in data) {
            window.location.href = SERVER_URL + '/login';
        }
    });

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
                        <Route path="/complete" element={<Complete chatId={chatId}/>}/>
                    </Routes>
                </div>
            </Router>
        </div>
    )
}

export default Home