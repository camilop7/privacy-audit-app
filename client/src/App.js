import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Layout from './components/Layout';
import ScanPage from './pages/ScanPage';
import PhoneTracker from './pages/PhoneTracker';
import EmergencyTracker from './pages/EmergencyTracker';
import AdminDashboard from './pages/AdminDashboard';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/scan" element={<ScanPage />} />
          <Route path="/phone" element={<PhoneTracker />} />
          <Route path="/emergency" element={<EmergencyTracker />} />
          <Route path="/admin-dashboard" element={<AdminDashboard />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
