import {
  combineReducers,
  applyMiddleware,
  legacy_createStore as createStore,
  compose,
} from "redux";

import thunk from "redux-thunk";
import logger from "redux-logger";

import savedNewsReducer from "./news";
import userReducer from "./user";
import authReducer from "./auth";

const rootReducer = combineReducers({
  savedNews: savedNewsReducer,
  user: userReducer,
  auth : authReducer
});

let enhancer = applyMiddleware(thunk);

if (process.env.NODE_ENV !== "production") {
  const composeEnhancers =
    window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
  enhancer = composeEnhancers(applyMiddleware(thunk, logger));
}

const store = (defaultState) => {
  return createStore(rootReducer, defaultState, enhancer);
};

export default store;
