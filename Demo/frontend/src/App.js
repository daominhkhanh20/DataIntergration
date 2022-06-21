import './App.css';
import {
    BrowserRouter,
    Routes,
    Route,
} from "react-router-dom";
import Home from "../src/page/home";
import Product from "../src/page/product"

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route exact path="/" element={<Home/>} />
                <Route path="/:id" element={<Product />}/>
            </Routes>
        </BrowserRouter>
    );
}

export default App;
