import React from "react"
import Arvin from "../img/Arvin Head.png"

const Search = () => {
    return (
        <div className="search">
            <div className="searchForm">
                <input type="text" placeholder="Find a user"/>
            </div>
            <div className="userChat">
                <img src={Arvin} alt=""/>
                <div className="userChatInfo">
                    <span>Arvin</span>
                </div>
            </div>
        </div>
    )
}

export default Search