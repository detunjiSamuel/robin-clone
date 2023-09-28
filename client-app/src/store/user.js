const SET_USER = "user/set";
const DELETE_USER = "user/delete";

const SET_PROFILE_IMAGE = "user/profileImage/set";
const REMOVE_PROFILE_IMAGE = "user/profileImage/remove";
const UPDATE_NETWORTH = "user/networth/update";

const API_BASE_AUTH = "/api/auth";
const API_BASE_USER = "/api/user";

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

  setProfileImage: (imageUrl) => {
    return {
      type: SET_PROFILE_IMAGE,
      imageUrl,
    };
  },

  removeProfileImage: () => {
    return {
      type: REMOVE_PROFILE_IMAGE,
    };
  },

  updateAccount: (updatedAccount) => {
    return {
      type: UPDATE_NETWORTH,
      updatedAccount,
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

export const uploadProfileImage = (file) => async (dispatch) => {
  const formData = new FormData();
  formData.append("file", file);

  const options = {
    method: "POST",
    body: formData,
  };

  const result = fetch(`${API_BASE_USER}/upload`, options)
    .then((res) => {
      if (res.ok) return res.json();

      throw Error("couldn't upload profile image");
    })
    .then((res) => {
      dispatch(storeDispatchs.setProfileImage(res.file));
      return true;
    })
    .catch((e) => {
      return false;
    });

  return result;
};

export const deleteProfileImage = () => async (dispatch) => {
  try {
    await fetch(`${API_BASE_USER}/upload`, { method: "DELETE" });
    dispatch(storeDispatchs.removeProfileImage());
    return true;
  } catch (e) {
    return false;
  }
};

export const updateNetworth =
  (symbol, name, transaction_type, quantity, price) => async (dispatch) => {
    const response = await fetch(`${API_BASE_USER}/transaction`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ symbol, name, transaction_type, quantity, price }),
    });

    if (response.ok) {
      const data = await response.json();
      dispatch(storeDispatchs.updateAccount(data));
      return data.networth;
    }
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
    case SET_PROFILE_IMAGE: {
      return {
        user: {
          ...state.user,
          imageUrl: action.imageUrl,
        },
      };
    }
    case REMOVE_PROFILE_IMAGE: {
      return {
        user: {
          ...state.user,
          imageUrl: null,
        },
      };
    }

    case UPDATE_NETWORTH: {
      const newState = { ...state };
      newState.user.assets = action.updatedAccount.assets;
      newState.user.networth = action.updatedAccount.networth;
      newState.user.totalStock = action.updatedAccount.totalStock;
      return newState;
    }
    default:
      return state;
  }
};

export default userReducer;
