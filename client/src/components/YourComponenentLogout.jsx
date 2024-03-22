import React from 'react';

class YourComponentLogout extends React.Component {
    handleClick = () => {
        // Redirect to the login page
        window.location.href = 'http://localhost:8080/logout';
        console.log("Logging out");
    }

    render() {
        return (
            <button id="logoutBtn" onClick={this.handleClick}>
                Logout
            </button>
        );
    }
}

export default YourComponentLogout;