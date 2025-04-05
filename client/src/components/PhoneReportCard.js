import React from 'react';

const getColor = (score) => {
  if (score >= 80) return 'green';
  if (score >= 50) return 'orange';
  if (score >= 30) return 'yellow';
  return 'red';
};

const PhoneReportCard = ({ data }) => {
  return (
    <div style={{
      marginTop: '20px',
      padding: '20px',
      background: '#fff',
      borderRadius: '12px',
      boxShadow: '0 0 12px rgba(0,0,0,0.1)',
      maxWidth: '600px'
    }}>
      <h3>📞 Report for {data.phone}</h3>
      <p><strong>Carrier:</strong> {data.carrier}</p>
      <p><strong>Country:</strong> {data.country}</p>
      <p><strong>Fraud Likelihood:</strong> {data.fraud_likelihood}</p>
      <p><strong>Blacklist Match:</strong> {data.blacklist_match ? 'Yes ❌' : 'No ✅'}</p>
      <p><strong>Risk Score:</strong> <span style={{ color: getColor(data.risk_score), fontWeight: 'bold' }}>{data.risk_score}</span></p>

      <h4>📄 Notes:</h4>
      <ul>
        {data.notes.map((note, i) => <li key={i}>{note}</li>)}
      </ul>
    </div>
  );
};

export default PhoneReportCard;
