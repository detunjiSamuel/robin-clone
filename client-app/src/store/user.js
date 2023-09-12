const SET_USER = "user/set";
const DELETE_USER = "user/delete";

const storeDispatchs = {
  setUser: (user) => {
    return {
      type: SET_USER,
      user,
    };
  },

  deleteUser: (user) => {
    return {
      type: DELETE_USER,
    };
  },
};

/** ACTIONS */


const userReducer = (state = {}, action) => {
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
