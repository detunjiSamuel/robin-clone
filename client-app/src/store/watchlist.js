const CREATE_WATCHLIST = "watchlist/create";
const DELETE_WATCHLIST = "watchlist/delete";
const EDIT_WATCHLIST = "watchlist/edit";

const GET_WATCHLIST = "watchlist/user/get";

const ADD_TO_WATCHLIST = "watchlist/stock/add";
const REMOVE_FROM_WATCHLIST = "watchlist/stock/remove";

const API_BASE_WATCHLIST = "/api/watchlists";

const storeDispatchs = {
  getWatchlist: (watchlists) => {
    return {
      type: GET_WATCHLIST,
      watchlists,
    };
  },
  createWatchlist: (watchlist) => {
    return {
      type: CREATE_WATCHLIST,
      watchlist,
    };
  },
  deleteWatchlist: (watchlist) => {
    return {
      type: DELETE_WATCHLIST,
      watchlist,
    };
  },
  addToWatchlist: (stock) => {
    return {
      type: ADD_TO_WATCHLIST,
      stock,
    };
  },
  removeFromWatchlist: (stock) => {
    return {
      type: REMOVE_FROM_WATCHLIST,
      stock,
    };
  },
  editWatchlist: (watchlist) => {
    return {
      type: EDIT_WATCHLIST,
      watchlist,
    };
  },
};

/** ACTIONS */

export const getUserwatchlists = (userId) => async (dispatch) => {
  const res = await fetch(`${API_BASE_WATCHLIST}/current`);
  if (res.ok) {
    const { watchlists } = await res.json();
    dispatch(storeDispatchs.getWatchlist(watchlists));
    return watchlists;
  }
};

export const createWatchlist = (userId, name) => async (dispatch) => {
  const res = await fetch(`${API_BASE_WATCHLIST}/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      userId,
      name,
    }),
  });
  if (res.ok) {
    const watchlist = await res.json();
    dispatch(storeDispatchs.createWatchlist(watchlist));
    return watchlist;
  }
  throw Error("Error creating watchlist");
};

export const deleteWatchlist = (watchlistId) => async (dispatch) => {
  const res = await fetch(`${API_BASE_WATCHLIST}/${watchlistId}`, {
    method: "DELETE",
  });
  if (res.ok) {
    const watchlist = await res.json();
    dispatch(storeDispatchs.deleteWatchlist(watchlistId));
    return watchlist;
  }
  throw Error("Error deleting watchlist");
};

export const addToWatchlist = (symbol, watchlist) => async (dispatch) => {
  const res = await fetch(`${API_BASE_WATCHLIST}/${watchlist}/stocks`, {
    method: "POST",
    body: JSON.stringify({ symbol }),
  });
  if (res.ok) {
    const stock = await res.json();
    dispatch(storeDispatchs.addToWatchlist(symbol));
    return stock;
  }
  throw Error("Error adding stock to watchlist");
};

export const removeFromWatchlist = (stock) => async (dispatch) => {
  const { stock_ticker } = stock;
  const res = await fetch(`${API_BASE_WATCHLIST}/stocks/${stock_ticker}`, {
    method: "DELETE",
  });
  if (res.ok) {
    const stock = await res.json();
    dispatch(storeDispatchs.removeFromWatchlist(stock));
    return stock;
  }
  throw Error("Error removing stock from watchlist");
};

export const editWatchlist = (watchlist_id, name) => async (dispatch) => {
  const res = await fetch(`${API_BASE_WATCHLIST}/${watchlist_id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ name }),
  });
  if (res.ok) {
    const watchlist = await res.json();
    dispatch(storeDispatchs.editWatchlist({ watchlist_id, name }));
    return watchlist;
  }
  throw Error("Error editing watchlist");
};

const watchlistReducer = (state = {}, action) => {
  let newState;
  switch (action.type) {
    case GET_WATCHLIST:
      const watchlists = {};
      action.watchlists.forEach((watchlist) => {
        watchlists[watchlist.id] = watchlist;
      });
      return {
        ...state,
        watchlists,
      };
    case CREATE_WATCHLIST:
      return {
        ...state,
        watchlists: {
          ...state.watchlists,
          [action.watchlist.id]: action.watchlist,
        },
      };
    case DELETE_WATCHLIST:
      newState = { ...state };
      delete newState.watchlists[action.watchlist];
      return newState;

    case ADD_TO_WATCHLIST:
      newState = { ...state };
      newState.watchlists[action.stock.watchlist_id].watchlist_stocks.push(
        action.stock
      );
      return newState;
    case REMOVE_FROM_WATCHLIST:
      newState = { ...state };
      const stockIdx = newState.watchlists[
        action.stock.watchlist_id
      ].watchlist_stocks.findIndex(
        (stock) => stock.symbol === action.stock.stock_ticker
      );

      newState.watchlists[action.watchlist.id].watchlist_stocks.splice(
        stockIdx,
        1
      );
      return newState;
    case EDIT_WATCHLIST:
      newState = { ...state };
      newState.watchlists[action.watchlist_id].name = action.name;
      return state;
    default:
      return state;
  }
};

export default watchlistReducer;
