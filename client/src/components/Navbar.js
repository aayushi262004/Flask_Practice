import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth, logout } from '../auth';

const LoggedInLinks = ({ onLogout }) => {
  return (
    <>
      <li className="nav-item">
        <Link className="nav-link active" to="/">Home</Link>
      </li>
      <li className="nav-item">
        <button className="nav-link btn btn-link text-white" onClick={onLogout}>LogOut</button>
      </li>
    </>
  );
};

const LoggedOutLinks = () => {
  return (
    <>
      <li className="nav-item">
        <Link className="nav-link active" to="/">Home</Link>
      </li>
      <li className="nav-item">
        <Link className="nav-link active" to="/signup">SignUp</Link>
      </li>
      <li className="nav-item">
        <Link className="nav-link active" to="/login">Login</Link>
      </li>
    </>
  );
};

const NavBar = () => {
  const [logged] = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();           // clear token
    navigate('/login'); // redirect to login
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
      <div className="container-fluid">
        <Link className="navbar-brand" to="/">Recipes</Link>
        <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
          aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav">
            {logged ? (
              <>
                <LoggedInLinks onLogout={handleLogout} />
                <li className="nav-item">
                  <Link className="nav-link active" to="/create_recipe">Create Recipes</Link>
                </li>
              </>
            ) : (
              <>
                <LoggedOutLinks />
              </>
            )}
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default NavBar;
