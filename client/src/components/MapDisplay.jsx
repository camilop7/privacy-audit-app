import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

const MapDisplay = ({ locations }) => {
  if (locations.length === 0) return <p>No emergency pings yet.</p>;

  return (
    <MapContainer
      center={[locations[0].lat, locations[0].lon]}
      zoom={4}
      style={{ height: '500px', width: '100%' }}
    >
      <TileLayer
        attribution="&copy; OpenStreetMap contributors"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {locations.map((loc, idx) => (
        <Marker key={idx} position={[loc.lat, loc.lon]}>
          <Popup>
            📍 <strong>{loc.city}, {loc.region}</strong><br />
            Country: {loc.country}<br />
            IP: {loc.ip}
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
};

export default MapDisplay;
