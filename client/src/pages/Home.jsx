import React from 'react'
import Chat from '../components/Chat.jsx'
import Topbar from '../components/Topbar.jsx'

const Home = () => {
    return (
        <div className='home'>
            <div className='container'>
                <Chat/>
            </div>
            <div className='topbar'>
                <Topbar/>
            </div>
        </div>
    )
}

export default Home