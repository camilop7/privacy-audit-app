// src/App.jsx
import React from 'react';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate
} from 'react-router-dom';

import Sidebar            from './components/Sidebar';
import NavBar             from './components/NavBar';
import PrivateRoute       from './components/PrivateRoute';

import HomePage           from './pages/HomePage';
import Login              from './pages/Login';
import ScanPage           from './pages/ScanPage';
import PhoneTracker       from './pages/PhoneTracker';
import EmergencyTracker   from './pages/EmergencyTracker';
import AdminDashboard     from './pages/AdminDashboard';
import BookingsDashboard  from './pages/BookingsDashboard';

function App() {
  return (
    <Router>
      {/* fixed sidebar */}
      <Sidebar />

      {/* main content area, shifted right by sidebar width */}
      <div style={{ marginLeft: '240px', transition: 'margin-left 0.3s' }}>
        <NavBar />

        <Routes>
          {/* PUBLIC */}
          <Route path="/"      element={<HomePage />} />
          <Route path="/login" element={<Login />} />

          {/* PROTECTED */}
          <Route
            path="/scan"
            element={
              <PrivateRoute>
                <ScanPage />
              </PrivateRoute>
            }
          />
          <Route
            path="/phone"
            element={
              <PrivateRoute>
                <PhoneTracker />
              </PrivateRoute>
            }
          />
          <Route
            path="/emergency"
            element={
              <PrivateRoute>
                <EmergencyTracker />
              </PrivateRoute>
            }
          />
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

          {/* catch-all: redirect unknown URLs back to home */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
