import React from 'react';

const RISK_LABELS = {
  eval_detected: "⚠️ Uses eval() — often abused in malware and obfuscated code",
  document_write_detected: "📄 Uses document.write() — can inject dynamic scripts",
  function_constructor_detected: "🧠 Uses Function() constructor — potentially dangerous",
  base64_detected: "🧬 Uses base64 encoding — could hide payloads",
  obfuscated_detected: "💣 Obfuscated code detected — packed or minified scripts",
  minified_detected: "📦 Single-line/minified script — harder to analyze"
};

const ReportDialog = ({ result, onClose }) => {
  if (!result) return null;

  const {
    url,
    status_code,
    headers = {},
    third_party_domains = [],
    script_analysis = {},
  } = result;

  const risk_score = script_analysis.risk_score ?? 0;
  const risk_breakdown = script_analysis.risk_breakdown ?? {};
  const external_scripts = script_analysis.external_scripts ?? [];

  const renderRiskBreakdown = () => {
    return Object.entries(risk_breakdown)
      .filter(([_, count]) => count > 0)
      .map(([key, count]) => (
        <li key={key}>
          {RISK_LABELS[key] || key} <strong>({count}x)</strong>
        </li>
      ));
  };

  return (
    <div style={{
      padding: '20px',
      background: '#fff',
      borderRadius: '12px',
      boxShadow: '0 0 12px rgba(0,0,0,0.1)',
      maxWidth: '750px',
      margin: '0 auto'
    }}>
      <h2>📄 Site Audit Summary</h2>
      <p><strong>URL:</strong> {url}</p>
      <p><strong>Status Code:</strong> {status_code}</p>
      <p><strong>Risk Score:</strong> {risk_score} / 100</p>

      <h3>🚨 Script Risk Breakdown</h3>
      {renderRiskBreakdown().length > 0 ? (
        <ul>{renderRiskBreakdown()}</ul>
      ) : (
        <p style={{ color: 'green' }}>✅ No suspicious inline script patterns detected.</p>
      )}

      <h3>🔗 Third-Party Domains</h3>
      <ul>
        {third_party_domains.map((domain, i) => (
          <li key={i}>{domain}</li>
        ))}
      </ul>

      <h3>📜 External Scripts</h3>
      <ul>
        {external_scripts.map((script, i) => (
          <li key={i}>
            {script.src}{" "}
            {script.is_third_party ? (
              <span style={{ color: "red", fontWeight: "bold" }}> (3rd-party)</span>
            ) : (
              <span style={{ color: "green" }}> (same domain)</span>
            )}
          </li>
        ))}
      </ul>

      <h3>📦 Headers</h3>
      <pre style={{
        background: '#f5f5f5',
        padding: '10px',
        borderRadius: '6px',
        maxHeight: '300px',
        overflow: 'auto'
      }}>
        {JSON.stringify(headers, null, 2)}
      </pre>

      <button onClick={onClose} style={{
        marginTop: '20px',
        padding: '10px 20px',
        background: '#333',
        color: '#fff',
        border: 'none',
        borderRadius: '6px',
        cursor: 'pointer'
      }}>
        Close Report
      </button>
    </div>
  );
};

export default ReportDialog;
