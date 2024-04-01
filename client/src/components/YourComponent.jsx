import React from 'react';
const SERVER_URL = process.env.SERVER_URL;
class YourComponent extends React.Component {
    handleClick = () => {
        // Redirect to the login page
        window.location.href = SERVER_URL + '/login';
        console.log("Logging in");
    }

    render() {
        return (
            <button id="loginBtn" onClick={this.handleClick}>
                Login
            </button>
        );
    }
}

export default YourComponent;