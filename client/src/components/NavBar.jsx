import React from 'react';
import { Link } from 'react-router-dom';

const NavBar = () => (
  <nav style={{ padding: '10px', borderBottom: '1px solid #ccc' }}>
    <Link to="/" style={{ marginRight: '15px' }}>Home</Link>
    <Link to="/scan">Scan</Link>
    <Link to="/bookings">Bookings</Link>
  </nav>
);

export default NavBar;
