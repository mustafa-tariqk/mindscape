import React from "react"
import Image from "../img/2.25+ KD Club logo.png"

const Navbar = () => {
    return (
        <div className="navbar">
            <span className="logo">Lama Chat</span>
            <div className="user">
                <img src={Image} alt="" />
                <span>Connor</span>
                <button>Log Out</button>
            </div>
        </div>
    )
}

export default Navbar