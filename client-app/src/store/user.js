

const SET_PROFILE_IMAGE = "user/profileImage/add";
const REMOVE_PROFILE_IMAGE = "user/profileImage/remove";
const ADD_NEW_TRANSACTION = "user/networth/update";


const API_BASE_USER = "/api/users";

const storeDispatchs = {

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
      type: ADD_NEW_TRANSACTION,
      updatedAccount,
    };
  },
};

/** ACTIONS */


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

export const addNewTransaction =
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
    case SET_PROFILE_IMAGE: {
      return {
        user: {
          imageUrl: action.imageUrl,
        },
      };
    }
    case REMOVE_PROFILE_IMAGE: {
      return {
        user: {  
          imageUrl: null,
        },
      };
    }

    case ADD_NEW_TRANSACTION: {
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
