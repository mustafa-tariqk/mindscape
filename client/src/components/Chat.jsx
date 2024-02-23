// Desc: This file contains the chat component which is the main component for the chat feature. 
// It contains the chat info, messages, and input components.
// It also contains the state for the messages and the function to set the messages.
import { useEffect, useState } from "react"

import Neuma from "/Users/ibrahim/Documents/GitHub/mindscape/client/src/img/Neuma Logo.png"
import Message from "./Message"
import Input from "./Input"

function Chat() { // This is the chat component
    const [messages, setMessages] = useState([])
    
    return (
        <div className="chat">
            <div className="chatInfo">
                <span>Neuma</span>
                <div className="chatIcons">
                    <img src={Neuma} alt="" />
                </div>
            </div>
            <div className='messages'>
                {messages.map(mess => (
                    <Message whoIsIt={mess.origin} passedMessage={mess.content} /> 
                ))}
            </div>
            <Input setMessages={setMessages} messageBank={messages}/>
        </div>
    )
}

export default Chat
//import React, { useState, useEffect } from 'react';

// function Chat() {
//     const [messages, setMessages] = useState([]);
  
//     useEffect(() => {
//       fetch('http://your-api-url/messages')
//         .then(response => response.json())
//         .then(data => setMessages(data));
//     }, []);
  
//     const postMessage = (message) => {
//       fetch('http://your-api-url/messages', {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({ message }),
//       })
//       .then(response => response.json())
//       .then(data => {
//         setMessages(prevMessages => [...prevMessages, data]);
//       });
//     };
  
//     return (
//       <div>
//         {messages.map((message, index) => (
//           <p key={index}>{message}</p>
//         ))}
//         <button onClick={() => postMessage('Your message here')}>Send</button>
//       </div>
//     );
//   }
  
//   export default Chat;