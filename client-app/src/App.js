import logo from "./logo.svg";
import "./App.css";
import "./css/global.css";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import LoginForm from "./components/auth/loginForm";
import ProtectedRoute from "./components/auth/ProtectedRoute";
import { useDispatch } from "react-redux";
import { authenticate } from "./store/auth";
import React, { useEffect } from "react";

import UserPage from "./components/UserPage";
import LandingNavBar from "./components/landingpage/navBar";
import LandingFooter from "./components/landingpage/footer";
import InvestPage from "./components/landingpage/InvestPage";
import LearnPage from "./components/landingpage/learnPage";
import Base from "./components/landingpage/Base";

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
        <Route
          path="/"
          element={
            <React.Fragment>
              <LandingNavBar />
              <Base />
              <LandingFooter />
            </React.Fragment>
          }
        />
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

        <Route
          path="/learn"
          element={
            <React.Fragment>
              <LandingNavBar />
              <LearnPage />
              <LandingFooter />
            </React.Fragment>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
