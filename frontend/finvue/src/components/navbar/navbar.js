// Navbar.js

import React from 'react';
import { Link } from 'react-router-dom';
import './navbar.css';

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="logo">
        <Link to="/">FinVue</Link>
      </div>
      <ul className="nav-links">
        <li><Link to="/transaction-dashboard">Transaction Dashboard</Link></li>
        <li><Link to="/stocks">Stocks</Link></li>
        <li><Link to="/budget">Budget</Link></li>
        <li><Link to="/savings">Savings</Link></li>
      </ul>
    </nav>
  );
}

export default Navbar;

