import { combineReducers } from "redux";
import home from "./home/index"

const myReducer = combineReducers({
    home: home
});

export default myReducer