import React, { useState, useEffect } from 'react';

const SERVER_URL = process.env.SERVER_URL;

const DownloadChatsButton = ({ userRole }) => {
    const [isAllowed, setIsAllowed] = useState(false);
    const [showDownloadButton, setShowDownloadButton] = useState(false); // State to toggle visibility

    useEffect(() => {
        // Check if the user's role is either administrator or researcher
        const allowedRoles = ['administrator', 'researcher'];
        setIsAllowed(allowedRoles);
    }, [userRole]);

    const download = (content, fileName, contentType) => {
        var a = document.createElement("a");
        var file = new Blob([content], {type: contentType});
        a.href = URL.createObjectURL(file);
        a.download = fileName;
        a.click();
    };

    const handleDownloadChats = async () => {
        try {
            const response = await fetch(`${SERVER_URL}/api/get_all_chats`, {
                method: 'GET',
                mode: 'cors',
                credentials: 'include',
            });
            if (!response.ok) {
                throw new Error('Failed to fetch chats');
            }
            const chats = await response.json();
            const fileName = 'all_chats.json';
            const jsonStr = JSON.stringify(chats, null, 2);
            download(jsonStr, fileName, 'application/json');
        } catch (error) {
            console.error('Error downloading chats:', error);
        }
    };

    const toggleDownloadButton = () => setShowDownloadButton(!showDownloadButton); // Toggle visibility

    return (
        <div className="download-chats-container">
            {isAllowed && (
                <button onClick={toggleDownloadButton} className='download-button-wrapper'>
                    {showDownloadButton ? 'Hide Download Button' : 'Show Download Button'}
                </button>
            )}
            {isAllowed && showDownloadButton && (
                <button onClick={handleDownloadChats} className='download-button'>
                    Download Chats
                </button>
            )}
        </div>
    );
};

export default DownloadChatsButton;
