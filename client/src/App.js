import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import ScanPage from './pages/ScanPage';
import PhoneTracker from './pages/PhoneTracker';
import EmergencyTracker from './pages/EmergencyTracker';
import AdminDashboard from './pages/AdminDashboard';
import Login from './pages/Login';
import PrivateRoute from './components/PrivateRoute'; // ✅ We'll create this next

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/login" element={<Login />} />

          {/* Protected Routes */}
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
            path="/admin-dashboard"
            element={
              <PrivateRoute>
                <AdminDashboard />
              </PrivateRoute>
            }
          />

          {/* Default route: redirect to login */}
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
