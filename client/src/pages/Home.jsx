import React from 'react'
import Chat from '../components/Chat'
import Topbar from '../components/Topbar'

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