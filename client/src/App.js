import React from "react";
import Home from "./pages/Home.jsx";
import Login from "./pages/Login.jsx";
import AdminHome from "./pages/AdminHome.jsx";
import Complete from "./pages/Complete.jsx";
import "./style.scss"

const SERVER_URL = process.env.SERVER_URL;

function App() {

  //Login check here
  fetch(SERVER_URL + '/api/user', {
    method: 'GET',
    mode: 'cors',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json'
    }
  })
    .then(response => response.json())
    .then(data => {
      if (data.hasOwnProperty('error')) {
        window.location.href = SERVER_URL + '/login';
      }
    });

  return (
    <Home />
  );
}

export default App;
