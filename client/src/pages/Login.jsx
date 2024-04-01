import Neuma from '../img/Logo_with_subtext_upscaled.png'
import User from '../img/userprofile.png'
import Wellness from '../img/wellness_background.png'
import React from 'react'
import YourComponent from '../components/YourComponent.jsx'
import { useEffect, useState } from 'react'

const SERVER_URL = process.env.SERVER_URL;

const Login = () => {

    const [disclaimerText, setDisclaimerText] = useState('');

    useEffect(() => {
        fetch('disclaimer.txt')
            .then((response) => response.text())
            .then((text) => {
                setDisclaimerText(text);
            });
    }, []);

    return (
        <div className='agreementScreen'>
            <div className='menubar'>
                <div className='left'>
                    <img src={Neuma} alt="Neuma Logo" />
                </div>
                <div className='middle'></div>
                <div className='right'>
                    <img src={User} alt="Image" />
                </div>
            </div>
            {/* Now for the screen components*/}
            <div className="page">
                <div className="background">
                    <img src={Wellness} alt="A Tranquil Background" />
                    <div className="content">
                        <h1>NEUMA Mindscape</h1>
                        <h2>Conversational AI Chatbot</h2>
                        <p>
                            {disclaimerText}
                        </p>
                        <div className='yourcomponent'>
                            <YourComponent/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Login;