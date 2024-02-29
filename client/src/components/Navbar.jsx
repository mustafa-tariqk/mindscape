// Desc: Navbar component for the chat app
import React from "react"
import User from "../img/userprofile.png";

const Navbar = () => {
    return (
        <div className="navbar">
            <span className="logo">Lama Chat</span>
            <div className="user">
                <img src={User} alt="" />
                <span>Connor</span>
                <button>Log Out</button>
            </div>
        </div>
    )
}

export default Navbar