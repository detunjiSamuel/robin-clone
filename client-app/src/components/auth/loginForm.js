import React, { useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import { Link, Navigate } from "react-router-dom";

import { login } from "../../store/user";

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

  if (user) {
    return <Navigate to="/" replace={true} />;
  }

  return <div>LOGIN PAGE</div>;
};

export default LoginForm;
