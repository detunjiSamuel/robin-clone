import React from "react";
import { useSelector } from "react-redux";
import { Navigate } from "react-router-dom";

const ProtectedRoute = (props) => {
  // const user = useSelector((state) => state.auth.user);
  const user =  localStorage.getItem('auth:user')

  return (
    <React.Fragment>
      {user ? props.children : <Navigate to="/login" replace={true} />}
    </React.Fragment>
  );
};

export default ProtectedRoute;
