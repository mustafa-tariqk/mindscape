import React from "react"
import Arvin from "../img/Arvin Head.png"
import Us from "../img/2.25+ KD Club logo.png"

const Message = ({key, whoIsIt, passedMessage}) => {
    return (
        <div className={`message ${whoIsIt === "me" && "owner"}`} key={origin + key}>
            {/* What this does is add multiple class names*/}
            <div className="messageInfo">
                <img src={whoIsIt === "me" ? Us : Arvin} alt=""/>
                <span>just now</span>
            </div>
            <div className="messageContent">
                <p>{passedMessage}</p>
            </div>
        </div>
    )
}

export default Message