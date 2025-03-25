import React from 'react';

const DisclaimerBox = () => (
  <div style={{
    backgroundColor: '#f9f9f9',
    padding: '15px',
    marginTop: '20px',
    border: '1px solid #ddd',
    borderRadius: '8px',
    fontSize: '14px'
  }}>
    ⚠️ <strong>Disclaimer:</strong> The risk score is an estimation based on visible tracking scripts,
    third-party domains, and inline JavaScript behavior. It does not represent malware or virus risk,
    but rather potential data exposure and privacy violations.
  </div>
);

export default DisclaimerBox;
