import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Leaflet fix
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

const EmergencyTracker = () => {
  const [location, setLocation] = useState(null);
  const [history, setHistory] = useState([]);
  const [error, setError] = useState(null);
  const [isPinging, setIsPinging] = useState(false);
  const [manualIP, setManualIP] = useState('');
  const [manualResult, setManualResult] = useState(null);
  const [showHistory, setShowHistory] = useState(false);
  const [deviceId, setDeviceId] = useState('');
  const [statusResult, setStatusResult] = useState(null);
  const [statusError, setStatusError] = useState('');
  const [isChecking, setIsChecking] = useState(false);

  const sendEmergencyPing = async () => {
    setIsPinging(true);
    setError(null);

    const screen = {
      width: window.innerWidth,
      height: window.innerHeight
    };

    navigator.geolocation.getCurrentPosition(async (position) => {
      const gps = {
        lat: position.coords.latitude,
        lon: position.coords.longitude
      };

      try {
        const res = await axios.post('http://localhost:8000/api/emergency/ping', {
          screen,
          gps
        });

        if (res.data.success) {
          setLocation(res.data.data);
          fetchLocationHistory();
        } else {
          setError('Ping failed');
        }
      } catch (err) {
        setError('Ping error: ' + err.message);
      } finally {
        setIsPinging(false);
      }
    }, async () => {
      // fallback if user blocks geolocation
      try {
        const res = await axios.post('http://localhost:8000/api/emergency/ping', { screen });
        if (res.data.success) {
          setLocation(res.data.data);
          fetchLocationHistory();
        }
      } catch (err) {
        setError('Ping error: ' + err.message);
      } finally {
        setIsPinging(false);
      }
    });
  };


  const fetchLocationHistory = async () => {
    try {
      const res = await axios.get('http://localhost:8000/api/emergency/locations');
      if (res.data.success) {
        setHistory(res.data.data);
      }
    } catch (err) {
      setError('Could not fetch location history.');
    }
  };

  const searchManualIP = async () => {
    if (!manualIP) return;
    setManualResult(null);
    setError(null);
    try {
      const res = await axios.get(`http://localhost:8000/api/emergency/ip-lookup/${manualIP}`);
      setManualResult(res.data);
    } catch (err) {
      setError('IP lookup failed: ' + err.message);
    }
  };

  const checkDeviceStatus = async () => {
    if (!deviceId) return;
    setIsChecking(true);
    setStatusError('');
    try {
      const res = await axios.get(`http://localhost:8000/api/emergency/check-status?device_id=${deviceId}`);
      setStatusResult(res.data);
    } catch (err) {
      console.error(err);
      setStatusError('Could not fetch status.');
    } finally {
      setIsChecking(false);
    }
  };

  useEffect(() => {
    fetchLocationHistory();
  }, []);

  const displayLocation = manualResult || location;

  return (
    <div style={{ padding: '20px', paddingBottom: '100px' }}>
      <h2>🆘 Emergency Tracker</h2>

      {/* Manual IP Lookup */}
      <div style={{ marginBottom: '20px' }}>
        <h3>🔍 Lookup IP Manually</h3>
        <input
          type="text"
          value={manualIP}
          onChange={(e) => setManualIP(e.target.value)}
          placeholder="Enter IP address"
          style={{ padding: '8px', width: '250px', marginRight: '10px' }}
        />
        <button onClick={searchManualIP} style={{
          padding: '8px 16px',
          background: '#2980b9',
          color: '#fff',
          border: 'none',
          borderRadius: '5px',
          cursor: 'pointer'
        }}>
          Search IP
        </button>
      </div>

      {manualResult && (
        <div style={{
          padding: '10px 15px',
          background: '#f8f8f8',
          borderRadius: '6px',
          marginBottom: '20px',
          border: '1px solid #ccc'
        }}>
          <p><strong>VPN:</strong> {manualResult.vpn ? 'Yes' : 'No'}</p>
          <p><strong>Org:</strong> {manualResult.org}</p>
          <p><strong>Hostname:</strong> {manualResult.hostname}</p>
        </div>
      )}

      {/* Location Details + Map */}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {displayLocation && (
        <div style={{
          marginTop: '20px',
          padding: '15px',
          border: '2px solid #ddd',
          borderRadius: '10px',
          background: '#f9f9f9'
        }}>
          <h3>📍 Last Known Location</h3>
          <p><strong>IP:</strong> {displayLocation.ip}</p>
          <p><strong>City:</strong> {displayLocation.city}</p>
          <p><strong>Region:</strong> {displayLocation.region}</p>
          <p><strong>Country:</strong> {displayLocation.country}</p>
          <p><strong>Latitude:</strong> {displayLocation.lat}</p>
          <p><strong>Longitude:</strong> {displayLocation.lon}</p>
          { !location && (
            <p style={{ color: 'orange' }}><em>Fallback location used</em></p>
          )}

          {displayLocation.lat && displayLocation.lon && (
            <div style={{ marginTop: '20px', height: '300px' }}>
              <MapContainer
                center={[displayLocation.lat, displayLocation.lon]}
                zoom={13}
                scrollWheelZoom={false}
                style={{ height: '100%', width: '100%', borderRadius: '10px' }}
              >
                <TileLayer
                  attribution='&copy; OpenStreetMap contributors'
                  url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                <Marker position={[displayLocation.lat, displayLocation.lon]}>
                  <Popup>
                    {manualResult ? 'Manual IP' : 'Emergency Ping'}: {displayLocation.city || 'Unknown'}
                  </Popup>
                </Marker>
              </MapContainer>
            </div>
          )}
        </div>
      )}

      {/* Live Tracker */}
      <div style={{ marginTop: '30px' }}>
        <h3>📡 Live Device Tracker</h3>
        <input
          type="text"
          placeholder="Enter device ID"
          value={deviceId}
          onChange={(e) => setDeviceId(e.target.value)}
          style={{ padding: '8px', width: '250px', marginRight: '10px' }}
        />
        <button onClick={checkDeviceStatus} style={{
          padding: '8px 16px',
          background: '#2c3e50',
          color: '#fff',
          border: 'none',
          borderRadius: '5px',
          cursor: 'pointer'
        }}>
          {isChecking ? 'Checking...' : 'Check Status'}
        </button>

        {statusError && <p style={{ color: 'red' }}>{statusError}</p>}

        {statusResult?.success && (
          <div style={{
            marginTop: '20px',
            padding: '15px',
            border: '2px solid #ccc',
            borderRadius: '10px',
            background: statusResult.alert_recommended ? '#fff0f0' : '#f0fff0'
          }}>
            <p><strong>Device:</strong> {statusResult.device_id}</p>
            <p><strong>Status:</strong> {statusResult.status.toUpperCase()}</p>
            <p><strong>Last Seen:</strong> {new Date(statusResult.last_seen).toLocaleString()}</p>
            <p><strong>Inactive For:</strong> {statusResult.inactive_for_minutes} min</p>
            <p><strong>IP:</strong> {statusResult.location.ip}</p>
            <p><strong>Lat:</strong> {statusResult.location.lat}</p>
            <p><strong>Lon:</strong> {statusResult.location.lon}</p>
            {statusResult.alert_recommended && (
              <p style={{ color: 'red', fontWeight: 'bold' }}>⚠️ No signal in 60+ min. Alert recommended!</p>
            )}
          </div>
        )}
      </div>

      {/* Emergency Ping History */}
      {history.length > 0 && (
        <div
          style={{
            marginTop: '30px',
            background: '#eee',
            borderRadius: '8px',
            padding: '10px',
            cursor: 'pointer',
            position: 'relative',
            width: 'fit-content'
          }}
          onMouseEnter={() => setShowHistory(true)}
          onMouseLeave={() => setShowHistory(false)}
        >
          <h3 style={{ margin: 0 }}>📜 Emergency Ping History</h3>
          {showHistory && (
            <ul style={{
              listStyle: 'none',
              marginTop: '10px',
              background: '#fff',
              padding: '10px',
              borderRadius: '6px',
              boxShadow: '0 2px 6px rgba(0,0,0,0.2)',
              position: 'absolute',
              top: '100%',
              zIndex: 10
            }}>
              {history.map((loc, i) => (
                <li key={i}>
                  {loc.ip} - {loc.city || 'Unknown'}, {loc.region || 'Unknown'}, {loc.country || 'Unknown'}
                </li>
              ))}
            </ul>
          )}
        </div>
      )}

      {/* Emergency Ping Button */}
      <div style={{
        position: 'fixed',
        bottom: '20px',
        left: '50%',
        transform: 'translateX(-50%)',
        zIndex: 1000
      }}>
        <button onClick={sendEmergencyPing} disabled={isPinging} style={{
          padding: '12px 24px',
          background: '#c0392b',
          color: '#fff',
          border: 'none',
          borderRadius: '8px',
          fontWeight: 'bold',
          fontSize: '16px',
          cursor: 'pointer',
          boxShadow: '0 4px 10px rgba(0,0,0,0.15)'
        }}>
          {isPinging ? 'Sending Ping...' : 'Send Emergency Ping'}
        </button>
      </div>
    </div>
  );
};

export default EmergencyTracker;
