import React from 'react';

class YourComponent extends React.Component {
    handleClick = () => {
        // Redirect to the login page
        window.location.href = 'http://localhost:8080/login';
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