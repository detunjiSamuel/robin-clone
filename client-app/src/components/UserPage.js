import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { useSelector } from "react-redux";


const UserPage = () => {
  const _user = useSelector((state) => state.auth.user);
  const [user, setUser] = useState({});
  
  const { user_id } = useParams();
  /**
   * TODO: change to allow to check other users
   */

  useEffect(() => {
   setUser(_user)
  }, [_user]);

  if (!user) {
    return <h1>Loading ... ....</h1>;
  }

  return (
    <React.Fragment>
      <ul>
        <li>
          <strong>User Id</strong> {user.id}
        </li>
        <li>
          <strong>Email</strong> {user.email}
        </li>
        <li>
          <strong>Joined at</strong> {user.joinedAt}
        </li>
      </ul>
    </React.Fragment>
  );
};

export default UserPage;
