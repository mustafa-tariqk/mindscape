// Desc: Search component for searching users
import React from "react"
import Neuma from "../img/Neuma Logo.png";

const Search = () => {
    return (
        <div className="search">
            <div className="searchForm">
                <input type="text" placeholder="Find a user"/>
            </div>
            <div className="userChat">
                <img src={Neuma} alt=""/>
                <div className="userChatInfo">
                    <span>Neuma</span>
                </div>
            </div>
        </div>
    )
}

export default Search