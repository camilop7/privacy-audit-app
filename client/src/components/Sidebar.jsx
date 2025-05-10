// src/components/Sidebar.jsx
import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';

export default function Sidebar() {
  const [isOpen, setIsOpen] = useState(true);
  const location = useLocation();
  const token = localStorage.getItem('token');

  // define which links are public vs protected
  const navItems = [
    { name: 'Home',             path: '/',           public: true },
    { name: 'Login',            path: '/login',      public: true },
    { name: 'Scan Website',     path: '/scan',       public: false },
    { name: 'Phone Scanner',    path: '/phone',      public: false },
    { name: 'Emergency Tracker',path: '/emergency',  public: false },
    { name: 'Users',            path: '/admin',      public: false },
    { name: 'Bookings',         path: '/bookings',   public: false },
  ];

  // only show public items if not logged in, else show all
  const itemsToShow = navItems.filter(item =>
    item.public || token
  );

  return (
    <div style={{
      position: 'fixed', top: 0, left: 0,
      width: isOpen ? '240px' : '60px',
      height: '100vh', background: '#1a1a1a',
      color: '#fff', overflow: 'hidden',
      transition: 'width 0.3s', zIndex: 999,
      boxShadow: '2px 0 8px rgba(0,0,0,0.2)'
    }}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        style={{
          background: 'none', color: '#fff', border: 'none',
          width: '100%', padding: '16px', textAlign: 'left',
          fontSize: '20px', cursor: 'pointer'
        }}
      >
        {isOpen ? '⏪' : '☰'}
      </button>

      {itemsToShow.map(item => (
        <Link
          key={item.path}
          to={item.path}
          style={{
            display: 'block',
            padding: '14px 20px',
            backgroundColor: location.pathname === item.path ? '#333' : 'transparent',
            color: '#fff',
            textDecoration: 'none'
          }}
        >
          {isOpen ? item.name : item.name.charAt(0)}
        </Link>
      ))}
    </div>
  );
}
