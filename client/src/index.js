import 'bootstrap/dist/css/bootstrap.min.css';
import './styles/main.css'
import React from 'react';
import ReactDOM from 'react-dom/client'; // <-- using the correct 'client' import
import {
  BrowserRouter as Router,
  Routes,
  Route
} from 'react-router-dom';

import NavBar from './components/Navbar';
import CreateRecipePage from './components/CreateRecipe';
import LoginPage from './components/Login';
import SignUpPage from './components/SignUp';
import HomePage from './components/Home';

const App = () => {
  return (
    <Router>
      <div className="">
        <NavBar />
        <Routes>
          <Route path="/create_recipe" element={<CreateRecipePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/signup" element={<SignUpPage />} />
          <Route path="/" element={<HomePage />} />
        </Routes>
      </div>
    </Router>
  );
};

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
