import React from "react"
import Arvin from "../img/Arvin Head.png"

const Chats = () => {
    return (
        <div className="chats">
            <div className="userChat">
                <img src={Arvin} alt=""/>
                <div className="userChatInfo">
                    <span>Arvin</span>
                    <p>Bro this video is ass</p>
                </div>
            </div>
            <div className="userChat">
                <img src={Arvin} alt=""/>
                <div className="userChatInfo">
                    <span>Arvin</span>
                    <p>Bro this video is ass</p>
                </div>
            </div>
            <div className="userChat">
                <img src={Arvin} alt=""/>
                <div className="userChatInfo">
                    <span>Arvin</span>
                    <p>Bro this video is ass</p>
                </div>
            </div>
        </div>
    )
}

export default Chats