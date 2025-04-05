import React, { useState } from 'react';
import axios from 'axios';
import MapDisplay from '../components/MapDisplay';

const EmergencyTracker = () => {
  const [locations, setLocations] = useState([]);
  const [sent, setSent] = useState(false);

  const sendPing = async () => {
    try {
      const res = await axios.post('http://localhost:8000/api/emergency/ping');
      if (res.data.success) {
        setSent(true);
        fetchLocations();
      }
    } catch (err) {
      console.error(err);
    }
  };

  const fetchLocations = async () => {
    try {
      const res = await axios.get('http://localhost:8000/api/emergency/locations');
      if (res.data.success) {
        setLocations(res.data.data);
      }
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>📡 Emergency Tracker</h2>
      <button onClick={sendPing} style={{ marginBottom: '20px' }}>
        Send Emergency Ping
      </button>

      {sent && <p style={{ color: 'green' }}>✅ Emergency ping sent successfully.</p>}

      <MapDisplay locations={locations} />
    </div>
  );
};

export default EmergencyTracker;
