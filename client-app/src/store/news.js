import { BASE_URL } from "./config"

const GET_SAVED_NEWS = "news/user/get";
const ADD_SAVED_NEWS = "news/user/add";
const DELETE_SAVED_NEWS = "news/user/delete";

const API_BASE_NEWS = BASE_URL +  "/api/news";

const storeDispatchs = {
  getSavedNews: (news) => {
    return {
      type: GET_SAVED_NEWS,
      news,
    };
  },

  addToSavedNews: (news) => {
    return {
      type: ADD_SAVED_NEWS,
      news,
    };
  },

  deleteSavedNews: (news) => {
    return {
      type: DELETE_SAVED_NEWS,
      news,
    };
  },
};

/** ACTIONS */

export const getSavedNews = () => async (dispatch) => {
  const response = await fetch(`${API_BASE_NEWS}/liked`);

  if (response.ok) {
    const news = await response.json();
    dispatch(storeDispatchs.getNews(news));
  }
};

export const addToSavedNews = (news) => async (dispatch) => {
  const response = await fetch(`${API_BASE_NEWS}/liked`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(news),
  });

  if (response.ok) {
    const news = await response.json();
    dispatch(storeDispatchs.addToSavedNews(news));
  }
};

export const deleteSavedNews = (news) => async (dispatch) => {
  const response = await fetch(`${API_BASE_NEWS}/liked/${news.id}`, {
    method: "DELETE",
  });

  if (response.ok) {
    dispatch(storeDispatchs.deleteSavedNews(news));
  }
};

const newsReducer = (state = {}, action) => {
  switch (action.type) {
    case GET_SAVED_NEWS: {
      const newState = { ...state };

      action.news.forEach((news) => {
        newState[news.id] = news;
      });

      return newState;
    }
    case ADD_SAVED_NEWS: {
      const newState = { ...state };

      newState[action.news.id] = action.news;

      return newState;
    }
    case DELETE_SAVED_NEWS: {
      const newState = { ...state };

      delete newState[action.news.id];

      return newState;
    }
    default:
      return state;
  }
};

export default newsReducer;
