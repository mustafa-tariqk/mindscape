// Desc: This file contains the input component for the chat app. 
// It allows the user to type a message and send it to the chat window.
// It also allows the user to send a file to the chat window.


import { useState } from 'react';

function Input({ onSendMessage }) {
    const [userInput, setUserInput] = useState('');

    const handleSubmit = (event) => {
        event.preventDefault(); // Prevent the form from submitting in the traditional way
        if (userInput.trim()) { // Check if the input is not just whitespace
            onSendMessage(userInput);
            setUserInput(''); // Clear the input after sending
        }
    };

    return (
        <form onSubmit={handleSubmit} className="input-area">
            <input
                type="text"
                id="message-input"
                placeholder="Enter your message..."
                value={userInput}
                onChange={(e) => setUserInput(e.target.value)}
                autoComplete="off" // Optionally disable autocomplete
            />
            <button type="submit" id="send-button">Send</button>
        </form>
    );
}

export default Input;









// import { useState } from "react"

// function Input({ onSendMessage }) {
//     const [userInput, setUserInput] = useState('');

//     const handleSubmit = (event) => {
//         event.preventDefault();
//         onSendMessage(userInput);
//         setUserInput(''); // Clear the input field after sending
//     };

//     return (
//         <form onSubmit={handleSubmit}>
//             <input
//                 type="text"
//                 value={userInput}
//                 onChange={(e) => setUserInput(e.target.value)}
//             />
//             <button type="submit">Send</button>
//         </form>
//     );
// }

// export default Input;







// import { useState } from "react"
// import Arvin from "../img/Arvin Head.png"

// function Input(props) {
//     const [currMessage, setCurrMessage] = useState("")
//     let messageBank = [...props.messageBank]

//     const handleSendMessage = () => {
//         if (currMessage.length > 0) {
//             messageBank.push({
//                 key: props.messageBank.length,
//                 content: currMessage, 
//                 origin: "me"
//             })
//             props.setMessages(messageBank)
//             setCurrMessage("")
//         }
//     }

//     return (
//         <div className="input">
//             <input 
//                 value={currMessage} 
//                 onInput={e => {setCurrMessage(e.target.value)}} 
//                 onKeyDown={ e => {
//                     if (e.code === "Enter" && currMessage.length > 0) {
//                         handleSendMessage()
//                     }
//                 }}
//                 type="text" 
//                 placeholder="Message Neuma..." 
//             />
//             <div className="send">
//                 <img src={Arvin} alt=""/>
//                 <input type="file" style={{display:"none"}} id="file" />
//                 <label htmlFor="file">
//                     <img src={Arvin} alt=""/>
//                 </label>
//                 <button onClick={handleSendMessage}>Send</button>
//             </div>
//         </div>
//     )
// }

// export default Input