import { BASE_URL } from "./config"

const SET_USER = "user/login";
const DELETE_USER = "user/logout";

const API_BASE_AUTH = BASE_URL + "/api/auth";

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

export const authenticate = () => async (dispatch) => {
  const response = await fetch(`${API_BASE_AUTH}/`, {
    headers: {
      "Content-Type": "application/json",
    },
  });
  if (response.ok) {
    const data = await response.json();
    if (data.errors) {
      return;
    }

    dispatch(storeDispatchs.setUser(data));
  }
};

export const signUp =
  (first_name, last_name, email, password, networth) => async (dispatch) => {
    const response = await fetch(`${API_BASE_AUTH}/signup`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        first_name,
        last_name,
        email,
        password,
        networth: networth,
      }),
    });

    if (response.ok) {
      const data = await response.json();

      dispatch(storeDispatchs.setUser(data));
    }
    if (response.status < 500) {
      const data = await response.json();
      if (data.errors) {
        return data.errors;
      }
    }
    return "internal server error";
  };

export const login = (email, password) => async (dispatch) => {
  try {
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
      if (data.errors) {
        return data.errors;
      }
    } else {
      return "internal server error";
    }
  } catch (e) {
    console.log(e);
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


const authReducer = (state = { user: null }, action) => {
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


export default authReducer