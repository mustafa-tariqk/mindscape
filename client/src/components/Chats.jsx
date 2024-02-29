// Desc: Chats component for the chat section of the dashboard
import React from "react"
import Neuma from "../img/Neuma Logo.png";

const Chats = () => {
    return (
        <div className="chats">
            <div className="userChat">
                <img src={Neuma} alt=""/>
                <div className="userChatInfo">
                    <span>Neuma</span>
                    <p>Bro this video is ass</p>
                </div>
            </div>
            <div className="userChat">
                <img src={Neuma} alt=""/>
                <div className="userChatInfo">
                    <span>Neuma</span>
                    <p>Bro this video is ass</p>
                </div>
            </div>
            <div className="userChat">
                <img src={Neuma} alt=""/>
                <div className="userChatInfo">
                    <span>Neuma</span>
                    <p>Bro this video is ass</p>
                </div>
            </div>
        </div>
    )
}

export default Chats