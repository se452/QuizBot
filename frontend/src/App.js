import React from "react";
import { Routes, Route } from "react-router-dom";
import Login from "./routes/login";
import Home from "./routes/home";
import Signup from "./routes/signup";
import { BrowserRouter } from "react-router-dom";

function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/home" element={<Home />} />
      </Routes>
    </>
  );
}

export default App;
