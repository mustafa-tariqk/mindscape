import React from 'react';
const SERVER_URL = process.env.SERVER_URL;

class YourComponentLogout extends React.Component {
    handleLogoutClick = () => {
        // Redirect to the logout page
        window.location.href = SERVER_URL + '/logout';
        console.log("Logging out");
    }

    handleLoginClick = () => {
        // Redirect to the login page
        window.location.href = SERVER_URL + '/login';
        console.log("Logging in");
    }

    render() {
        return (
            <div>
                <button id="logoutBtn" onClick={this.handleLogoutClick}>
                    Logout
                </button>
                <button id="loginBtn" onClick={this.handleLoginClick}>
                    Login
                </button>
            </div>
        );
    }
}

export default YourComponentLogout;