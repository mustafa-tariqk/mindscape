import { useState } from "react"
import Arvin from "../img/Arvin Head.png"

function Input(props) {
    const [currMessage, setCurrMessage] = useState("")
    let messageBank = [...props.messageBank]

    const handleSendMessage = () => {
        if (currMessage.length > 0) {
            messageBank.push({
                key: props.messageBank.length,
                content: currMessage, 
                origin: "me"
            })
            props.setMessages(messageBank)
            setCurrMessage("")
        }
    }

    return (
        <div className="input">
            <input 
                value={currMessage} 
                onInput={e => {setCurrMessage(e.target.value)}} 
                onInputCapture={ e => {
                    if (e.key === "Enter" && currMessage.length > 0) {
                        handleSendMessage()
                    }
                }}
                type="text" 
                placeholder="Type Something Here..." 
            />
            <div className="send">
                <img src={Arvin} alt=""/>
                <input type="file" style={{display:"none"}} id="file" />
                <label htmlFor="file">
                    <img src={Arvin} alt=""/>
                </label>
                <button onClick={handleSendMessage}>Send</button>
            </div>
        </div>
    )
}

export default Input