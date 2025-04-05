import React, { useState } from 'react';
import Layout from '../components/Layout';
import axios from 'axios';

const PhoneTracker = () => {
  const [phone, setPhone] = useState('');
  const [result, setResult] = useState(null);

  const handleScan = async () => {
    try {
      const res = await axios.get(`http://localhost:8000/api/phone/scan-phone?phone=${encodeURIComponent(phone)}`);
      setResult(res.data.data);
    } catch (err) {
      console.error(err);
      alert("Failed to scan phone number.");
    }
  };

  return (
    <Layout>
      <h2>☎️ Phone Scanner</h2>
      <input
        value={phone}
        onChange={(e) => setPhone(e.target.value)}
        placeholder="Enter phone number"
        style={{ padding: '8px', marginRight: '10px', width: '300px' }}
      />
      <button onClick={handleScan}>Scan</button>

      {result && (
        <div style={{
          marginTop: '20px',
          border: '1px solid #ccc',
          padding: '20px',
          borderRadius: '8px',
          background: '#f9f9f9'
        }}>
          <h3>📋 Result</h3>
          <p><strong>Phone:</strong> {result.phone}</p>
          <p><strong>Carrier:</strong> {result.carrier}</p>
          <p><strong>Country:</strong> {result.country}</p>
          <p><strong>Blacklist:</strong> {result.blacklist_match ? '⚠️ Yes' : '✅ No'}</p>
          <p><strong>Fraud Likelihood:</strong> {result.fraud_likelihood}</p>
          <p><strong>Risk Score:</strong>
            <span style={{
              fontWeight: 'bold',
              color:
                result.risk_score >= 75 ? 'red' :
                result.risk_score >= 50 ? 'orange' :
                result.risk_score >= 30 ? 'gold' :
                'green'
            }}>
              {' '}{result.risk_score} / 100
            </span>
          </p>
        </div>
      )}
    </Layout>
  );
};

export default PhoneTracker;
