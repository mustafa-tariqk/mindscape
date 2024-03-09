import React from "react";
import Home from "./pages/Home.jsx";
import Login from "./pages/Login.jsx";
import AdminHome from "./pages/AdminHome.jsx";
import Complete from "./pages/Complete.jsx";
import "./style.scss"

const SERVER_URL = process.env.SERVER_URL;

function App() {
  return (
    <Home />
  );
}

export default App;
