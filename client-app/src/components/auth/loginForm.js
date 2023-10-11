import React, { useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import { Link, Navigate } from "react-router-dom";

import { login } from "../../store/auth";

import "../../css/login.css";

const LoginForm = () => {
  const [errors, setErrors] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const user = useSelector((state) => state.auth.user);

  const dispatch = useDispatch();

  const onLogin = async (e) => {
    e.preventDefault();

    if (!email || !password) {
      setErrors("Please fill out all fields");
      return;
    }
    const returnedError = await dispatch(login(email, password));

    if (returnedError) {
      setErrors(returnedError);
    }
  };

  if (user) {
    return <Navigate to="/" replace={true} />;
  }
  return (
    <div className="login-page">
      <div className="login-page-left">LEFT</div>
      <div className="login-page-right">
        <div className="login-form-container">
          <h1 id="login-title"> Log into account </h1>
          <form id="login-form" onSubmit={onLogin}>
            <div className="login-form-input">
              <label htmlFor="email">Email</label>
              <input
                name="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>

            <div className="login-form-input">
              <label htmlFor="password">Password</label>
              <input
                name="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
            {errors && <div id= "login-failed-text">{errors}</div>}
            <button type="submit" id="login-submit">
              Login
            </button>
          </form>
          <Link to="/register">
            <p id="login-create-account">
              Don't have an account?{" "}
              <span id="create-an-account">Create an account</span>
            </p>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default LoginForm;
