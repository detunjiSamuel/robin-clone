import logo from "./logo.svg";
import "./App.css";
import "./css/global.css";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import LoginForm from "./components/auth/loginForm";
import ProtectedRoute from "./components/auth/ProtectedRoute";
import { useDispatch } from "react-redux";
import { authenticate, logout } from "./store/auth";
import React, { useEffect } from "react";

import UserPage from "./components/UserPage";
import LandingNavBar from "./components/landingpage/navBar";
import LandingFooter from "./components/landingpage/footer";
import InvestPage from "./components/landingpage/InvestPage";

function Base() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

function ProtectedBase() {
  return <div className="App">THIS IS Protected Page testing</div>;
}

function App() {
  const dispatch = useDispatch();

  useEffect(() => {
    (async () => {
      await dispatch(authenticate());
    })();
  }, [dispatch]);

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Base />} />
        <Route path="/login" element={<LoginForm />} />

        <Route
          path="/protected"
          element={
            <ProtectedRoute>
              <ProtectedBase />
            </ProtectedRoute>
          }
        />

        <Route
          path="/users/:user_id"
          element={
            <ProtectedRoute>
              <UserPage />
            </ProtectedRoute>
          }
        />

        <Route
          path="/invest"
          element={
            <React.Fragment>
              <LandingNavBar />
              <InvestPage />
              <LandingFooter />
            </React.Fragment>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
