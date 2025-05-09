// src/App.jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import HomePage           from './pages/HomePage';
import ScanPage           from './pages/ScanPage';
import Login              from './pages/Login';
import AdminDashboard     from './pages/AdminDashboard';
import BookingsDashboard  from './pages/BookingsDashboard';

import NavBar      from './components/NavBar';
import PrivateRoute from './components/PrivateRoute';
import Sidebar  from './components/Sidebar';

function App() {
  return (
    <Router>
      <Sidebar />
      <NavBar />

      <Routes>
        {/* public */}
        <Route path="/"        element={<HomePage />} />
        <Route path="/scan"    element={<ScanPage />} />
        <Route path="/login"   element={<Login />} />

        {/* protected */}
        <Route
          path="/admin"
          element={
            <PrivateRoute>
              <AdminDashboard />
            </PrivateRoute>
          }
        />
        <Route
          path="/bookings"
          element={
            <PrivateRoute>
              <BookingsDashboard />
            </PrivateRoute>
          }
        />

        {/* optional: 404 catch-all here */}
      </Routes>
    </Router>
  );
}

export default App;
