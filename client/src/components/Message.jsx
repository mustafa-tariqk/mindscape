// Desc: This component is used to display the messages in the chat. 
// It takes in the whoIsIt prop to determine if the message is from the user or the bot.
// It also takes in the passedMessage prop to display the message.
// It also takes in the key prop to keep track of the messages.
// It also uses the Neuma and Us images to display the user and bot images.
// It also uses the messageInfo and messageContent divs to display the message and the time it was sent.
// It also uses the owner class to determine if the message is from the user or the bot.
// It also uses the just now span to display the time the message was sent.
import Neuma from "../img/Neuma Logo.png";
import User from "../img/userprofile.png";

const Message = ({ whoIsIt, passedMessage }) => {
    return (
        <div className={`message ${whoIsIt === "me" ? "owner" : ""}`}>
            <div className="messageInfo">
                <img src={whoIsIt === "me" ? User : Neuma} alt="" />
            </div>
            <div className="messageContent">
                <p>{passedMessage}</p>
            </div>
        </div>
    );
};

export default Message;