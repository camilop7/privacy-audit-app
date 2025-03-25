import React, { useState } from 'react';
import axios from 'axios';
import ScanResultCard from '../components/ScanResultCard';
import ReportDialog from '../components/ReportDialog';

const ScanPage = () => {
  const [url, setUrl] = useState('');
  const [result, setResult] = useState(null);
  const [showReport, setShowReport] = useState(false);

  const handleScan = async () => {
    setResult(null);
    try {
      const res = await axios.get(`http://localhost:8000/api/scan?url=${encodeURIComponent(url)}`);
      setResult(res.data);
    } catch (err) {
      console.error(err);
      setResult({ error: 'Failed to scan the website.' });
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>🧪 Scan a Website</h2>
      <input
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        placeholder="https://example.com"
        style={{ width: '300px', padding: '8px', marginRight: '10px' }}
      />
      <button onClick={handleScan}>Scan</button>

      {result && !result.error && (
        <>
          <ScanResultCard result={result} onViewReport={() => setShowReport(true)} />
          <ReportDialog isOpen={showReport} result={result} onClose={() => setShowReport(false)} />
        </>
      )}

      {result?.error && (
        <p style={{ marginTop: '20px', color: 'red' }}>{result.error}</p>
      )}
    </div>
  );
};

export default ScanPage;
