import React, { useState } from 'react';
import axios from 'axios';

const ScanPage = () => {
  const [url, setUrl] = useState('');
  const [result, setResult] = useState(null);

  const handleScan = async () => {
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

      {result && (
        <div style={{ marginTop: '20px' }}>
          <h3>🔎 Scan Result</h3>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default ScanPage;
