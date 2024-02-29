// Desc: This file contains the chat component which is the main component for the chat feature. 
// It contains the chat info, messages, and input components.
// It also contains the state for the messages and the function to set the messages.
// import { useEffect, useState } from "react"

// import Neuma from "/Users/ibrahim/Documents/GitHub/mindscape/client/src/img/Neuma Logo.png"
// import Message from "./Message"
// import Input from "./Input"
// import ChatComponent from "./ChatCompnonent"

import { useEffect, useState } from "react";
import Neuma from "/Users/ibrahim/Documents/GitHub/mindscape/client/src/img/Neuma Logo.png";
import Message from "./Message";
import Input from "./Input";

function Chat() {
    const [messages, setMessages] = useState([]);
    const [chatId, setChatId] = useState(null);

    useEffect(() => {
        // Replace 'http://127.0.0.1:8080/' with your actual API endpoint
        fetch('http://127.0.0.1:8080/') 
            .then(response => response.json())
            .then(data => {
                const userId = data.user_id;
                startChat(userId);
            });
    }, []);

    function startChat(userId) {
        fetch('http://127.0.0.1:8080/start_chat/' + userId)
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
        fetch('http://127.0.0.1:8080/converse/', {
            method: 'POST',
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

    return (
        <div className="chat">
            <div className="chatInfo">
                <span>Neuma</span>
                <div className="chatIcons">
                    <img src={Neuma} alt="" />
                </div>
            </div>
            <div className='messages'>
                {messages.map((mess, index) => (
                    <Message key={index} whoIsIt={mess.origin} passedMessage={mess.content} /> 
                ))}
            </div>
            <Input onSendMessage={handleSendMessage}/>
        </div>
    );
}

export default Chat;













// import { useEffect, useState } from "react";
// import Neuma from "/Users/ibrahim/Documents/GitHub/mindscape/client/src/img/Neuma Logo.png";
// import Message from "./Message";
// import Input from "./Input";

// function Chat() {
//     const [messages, setMessages] = useState([]);

//     const handleSendMessage = async (userInput) => {
//         // Append the user message to the chat
//         const updatedMessages = [...messages, { origin: 'User', content: userInput }];
//         setMessages(updatedMessages);

//         try {
//             const response = await fetch('http://127.0.0.1:8080/', {
//                 method: 'POST',
//                 headers: {
//                     'Content-Type': 'application/json',
//                 },
//                 body: JSON.stringify({ message: userInput }),
//             });

//             if (!response.ok) {
//                 throw new Error(`HTTP error! status: ${response.status}`);
//             }

//             const data = await response.json();

//             // Assuming the response contains a message field
//             setMessages(prevMessages => [...prevMessages, { origin: 'Chatbot', content: data.message }]);
//         } catch (error) {
//             console.error("Failed to send message: ", error);
//             // Optionally handle the error by displaying a message to the user
//         }
//     };

//     return (
//         <div className="chat">
//             <div className="chatInfo">
//                 <span>Neuma</span>
//                 <div className="chatIcons">
//                     <img src={Neuma} alt="" />
//                 </div>
//             </div>
//             <div className='messages'>
//                 {messages.map((mess, index) => (
//                     <Message key={index} whoIsIt={mess.origin} passedMessage={mess.content} /> 
//                 ))}
//             </div>
//             <Input onSendMessage={handleSendMessage}/>
//         </div>
//     );
// }

// export default Chat;






// function Chat() { // This is the chat component
//     const [messages, setMessages] = useState([])
    
//     return (
//         <div className="chat">
//             <div className="chatInfo">
//                 <span>Neuma</span>
//                 <div className="chatIcons">
//                     <img src={Neuma} alt="" />
//                 </div>
//             </div>
//             <div className='messages'>
//                 {messages.map(mess => (
//                     <Message whoIsIt={mess.origin} passedMessage={mess.content} /> 
//                 ))}
//             </div>
//             <Input setMessages={setMessages} messageBank={messages}/>
//         </div>
//     )
// }

// export default Chat

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