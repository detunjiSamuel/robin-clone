import React, { useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import { Link, Navigate } from "react-router-dom";

import { login } from "../../store/user";

import leftImage from "../../images/login-image.jpeg";

const LoginForm = () => {
  const [errors, setErrors] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const user = useSelector((state) => state.user.user);

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

  const fakeLogin = async (e) => {
    e.preventDefault();

    const testEmail = "test123@test.com";
    const testPass = "testing1234";

    const returnedError = await dispatch(login(testEmail, testPass));

    if (returnedError) {
      setErrors(returnedError);
    }
  };

  if (user) {
    return <Navigate to="/" replace={true} />;
  }

  return (
    <div>
      LOGIN PAGE
      <form onSubmit={onLogin}>
        <div>
          <label htmlFor="email">Email</label>
          <input
            name="email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>

        <div>
          <label htmlFor="password">Password</label>
          <input
            name="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        {errors && <div>{errors}</div>}
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default LoginForm;
