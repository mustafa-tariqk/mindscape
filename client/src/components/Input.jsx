// Desc: This file contains the input component for the chat app. 
// It allows the user to type a message and send it to the chat window.
// It also allows the user to send a file to the chat window.
import React, { useState } from 'react';

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
        <div className='input'>
            <form onSubmit={handleSubmit} className="input-area">
                <input
                    type="text"
                    id="message-input"
                    placeholder="Enter your message..."
                    value={userInput}
                    onChange={(e) => setUserInput(e.target.value)}
                    autoComplete="off" // Optionally disable autocomplete
                />
                <div className='send'>
                    <button type="submit" id="send-button">Send</button>
                </div>
            </form>
        </div>
    );
}

export default Input;