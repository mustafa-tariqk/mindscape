import { useEffect, useState } from "react"

import Arvin from "../img/2.25+ KD Club logo.png"
import Message from "./Message"
import Input from "./Input"

function Chat() {
    const [messages, setMessages] = useState([
        {key: 0, content: "Hello", origin: "them"},
        {key: 1, content: "Hello you fuck", origin: "me"},
        {key: 2, content: "When is the video coming out", origin: "me"},
    ])

    return (
        <div className="chat">
            <div className="chatInfo">
                <span>Arvin</span>
                <div className="chatIcons">
                    <img src={Arvin} alt="" />
                    <img src={Arvin} alt="" />
                    <img src={Arvin} alt="" />
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