import logo from "./logo.svg";
import "./App.css";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import LoginForm from "./components/auth/loginForm";
import ProtectedRoute from "./components/auth/ProtectedRoute";

function Base() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

function ProtectedBase() {
  return <div className="App">THIS IS  Protected Page testing</div>;
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route exact path="/" element={<Base />} />
        <Route exact path="/login" element={<LoginForm />} />

        <Route
          exact
          path="/protected"
          element={
            <ProtectedRoute>
              <ProtectedBase />
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
