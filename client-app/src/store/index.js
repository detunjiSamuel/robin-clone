import {
  combineReducers,
  applyMiddleware,
  legacy_createStore as createStore,
  compose,
} from "redux";

import thunk from "redux-thunk";
import logger from "redux-logger";

const rootReducer = combineReducers({});

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
