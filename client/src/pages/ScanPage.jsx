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
    <div className="main-content">
      <div className="scan-container">
        <h2>🌐 Website Privacy Scanner</h2>
        <div className="scan-input-group">
          <input
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://example.com"
          />
          <button onClick={handleScan}>Scan</button>
        </div>

        {result && !result.error && (
          <>
            <ScanResultCard result={result} onViewReport={() => setShowReport(true)} />
            <ReportDialog isOpen={showReport} result={result} onClose={() => setShowReport(false)} />
          </>
        )}

        {result?.error && (
          <p className="error-message">{result.error}</p>
        )}
      </div>
    </div>
  );
};

export default ScanPage;
