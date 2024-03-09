// Desc: This file contains the chat component which is the main component for the chat feature. 
// It contains the chat info, messages, and input components.
// It also contains the state for the messages and the function to set the messages.
import React, { useEffect, useState } from "react";
import Message from "./Message.jsx";
import Input from "./Input.jsx";
import { Link, useNavigate } from "react-router-dom"

const SERVER_URL = process.env.SERVER_URL;

function Chat({chatId, setChatId}) {
    const [messages, setMessages] = useState([]);
    const navigate = useNavigate()

    useEffect(() => {
        fetch(SERVER_URL+'/api/user', {
            mode: 'cors',
            credentials: 'include',
        })
        .then(response => response.json())
        .then(data => {
            const userId = data.user_id;
            startChat(userId);
        });
    }, []);

    function startChat(userId) {
        fetch(SERVER_URL+'/api/start_chat/' + userId, {
            mode: 'cors',
            credentials: 'include',
        })
        .then(response => response.json())
        .then(data => {
            setChatId(data.chat_id);
        });
    }

    const handleSendMessage = (userInput) => {
        if (!chatId) {
            console.error("Chat ID is not set.");
            return;
        }
        const messageToSend = { chat_id: chatId, message: userInput };
        fetch(SERVER_URL+'/api/converse', {
            method: 'POST',
            mode: 'cors',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(messageToSend)
        })
        .then(response => response.json())
        .then(data => {
            setMessages(prevMessages => [...prevMessages, { origin: 'AI', content: data.ai_response }]);
        });

        // Also add the user message to the chat history
        setMessages(prevMessages => [...prevMessages, { origin: 'me', content: userInput }]);
    };

    const handleSubmit = () => {
        navigate("/complete")
    }

    return (
        <div className="chat">
            {/*
            <div className="chatInfo">
                <span>Neuma</span>
                <div className="chatIcons">
                    <img src={Neuma} alt="" />
                </div>
            </div>
            */}
            <div className='messages'>
                {messages.map((mess, index) => (
                    <Message key={index} whoIsIt={mess.origin} passedMessage={mess.content} /> 
                ))}
            </div>
            <Input onSendMessage={handleSendMessage}/>
            <div className="submit-convo">
                {/* <Link to="/complete" type="submit" id="submit">Submit Conversation</Link> */}
                <button type="submit" id="submit" onClick={handleSubmit}>SUBMIT CONVERSATION</button>
            </div>
        </div>
    );
}

export default Chat;