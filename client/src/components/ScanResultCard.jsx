import React from 'react';
import RiskBadge from './RiskBadge';
import DisclaimerBox from './DisclaimerBox';

const ScanResultCard = ({ result, onViewReport }) => {
  const { url, status_code, third_party_domains, script_analysis, risk_score } = result;

  // ✅ Detect if it's a .onion domain
  const isOnionDomain = (url) => {
    try {
      return new URL(url).hostname.endsWith('.onion');
    } catch {
      return false;
    }
  };

  return (
    <div style={{
      padding: '20px',
      border: '1px solid #ccc',
      marginTop: '20px',
      borderRadius: '10px',
      background: '#fff',
    }}>
      <h3>
        🔎 Scan Result for: <code>{url}</code>
        {isOnionDomain(url) && (
          <span style={{
            marginLeft: '10px',
            backgroundColor: '#333',
            color: '#fff',
            padding: '3px 8px',
            borderRadius: '6px',
            fontSize: '12px'
          }}>
            🧅 Dark Web Site
          </span>
        )}
      </h3>

      <p>Status Code: {status_code}</p>
      <RiskBadge score={risk_score} />
      <p style={{ marginTop: '10px' }}>
        Third-party domains: {third_party_domains.length}
        <br />
        Scripts detected: {script_analysis.total_scripts}
      </p>
      <button onClick={onViewReport}>📄 View Report Summary</button>

      <DisclaimerBox />

      {isOnionDomain(url) && (
        <div style={{
          marginTop: '15px',
          padding: '10px',
          backgroundColor: '#fff8e1',
          borderLeft: '5px solid orange',
          fontSize: '14px'
        }}>
          ⚠️ You are viewing a scan result for a <strong>.onion</strong> (Tor hidden service) domain. These sites may be anonymous, harder to trace, and less regulated.
          <br />
          Proceed with caution when interacting with unknown dark web resources.
        </div>
      )}
    </div>
  );
};

export default ScanResultCard;
