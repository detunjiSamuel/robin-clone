const SET_USER = "user/set";
const DELETE_USER = "user/delete";

const API_BASE_AUTH = "/api/auth";

const storeDispatchs = {
  setUser: (user) => {
    return {
      type: SET_USER,
      user,
    };
  },

  deleteUser: () => {
    return {
      type: DELETE_USER,
    };
  },
};

/** ACTIONS */

// signup

// login

export const login = (email, password) => async (dispatch) => {
  const response = await fetch(`${API_BASE_AUTH}/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password }),
  });

  if (response.ok) {
    const user = await response.json();
    dispatch(storeDispatchs.setUser(user));
  } else if (response.status < 500) {
    const data = await response.json();
    if (data.error) {
      return data.error;
    }
  } else {
    return "internal server error";
  }
};

export const logout = () => async (dispatch) => {
  const response = await fetch(`${API_BASE_AUTH}/logout`, {
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (response.ok) dispatch(storeDispatchs.deleteUser());
};

const userReducer = (state = { user: null }, action) => {
  switch (action.type) {
    case SET_USER: {
      return {
        user: action.user,
      };
    }
    case DELETE_USER: {
      return {
        user: null,
      };
    }
    default:
      return state;
  }
};

export default userReducer;
