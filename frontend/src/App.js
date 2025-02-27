import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import Login from "./routes/login";
import Home from "./routes/home";
import Signup from "./routes/signup";
import { BrowserRouter } from "react-router-dom";

function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/home" element={<Home />} />
        {/* Redirect any unknown routes to home */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </>
  );
}

export default App;
