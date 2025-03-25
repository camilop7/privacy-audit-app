import React from 'react';

const RiskBadge = ({ score }) => {
  const getColor = () => {
    if (score < 30) return 'green';
    if (score < 70) return 'orange';
    return 'red';
  };

  return (
    <span style={{
      padding: '4px 10px',
      backgroundColor: getColor(),
      color: '#fff',
      borderRadius: '5px',
      fontWeight: 'bold'
    }}>
      Risk Score: {score}
    </span>
  );
};

export default RiskBadge;
