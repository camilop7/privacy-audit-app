// src/components/Sidebar.jsx
import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';

const Sidebar = () => {
  const [isOpen, setIsOpen] = useState(true);
  const location = useLocation();

  const toggleSidebar = () => setIsOpen(!isOpen);

  const navItems = [
    { name: 'Scan Website',      path: '/scan' },
    { name: 'Phone Scanner',     path: '/phone' },
    { name: 'Emergency Tracker', path: '/emergency' },
    { name: 'Users',             path: '/admin' },      // matches /admin above
    { name: 'Bookings',          path: '/bookings' }    // matches /bookings above
  ];


  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: isOpen ? '240px' : '60px',
        height: '100vh',
        background: '#1a1a1a',
        color: '#fff',
        transition: 'width 0.3s',
        overflow: 'hidden',
        zIndex: 999,
        boxShadow: '2px 0 8px rgba(0,0,0,0.2)'
      }}
    >
      <button
        onClick={toggleSidebar}
        style={{
          background: 'none',
          color: '#fff',
          border: 'none',
          padding: '16px',
          fontSize: '20px',
          cursor: 'pointer',
          width: '100%',
          textAlign: 'left'
        }}
      >
        {isOpen ? '⏪' : '☰'}
      </button>

      {navItems.map(item => (
        <Link
          key={item.name}
          to={item.path}
          style={{
            display: 'block',
            padding: '14px 20px',
            backgroundColor: location.pathname === item.path ? '#333' : 'transparent',
            textDecoration: 'none',
            color: '#fff',
            transition: 'background 0.2s ease-in-out'
          }}
        >
          {isOpen ? item.name : item.name[0]}
        </Link>
      ))}
    </div>
  );
};

export default Sidebar;
