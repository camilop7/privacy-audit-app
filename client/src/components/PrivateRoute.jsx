import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';

function decodeJwtPayload(token) {
  try {
    const [, payload] = token.split('.');
    const json = atob(payload.replace(/-/g, '+').replace(/_/g, '/'));
    return JSON.parse(decodeURIComponent(escape(json)));
  } catch { return null; }
}

export default function PrivateRoute({ children }) {
  const loc = useLocation();
  const token = localStorage.getItem('access_token');
  console.log('🔒 PrivateRoute:', loc.pathname, 'token=', token?.slice(0,20) + '…');

  if (!token) return <Navigate to="/login" replace state={{ from: loc }} />;

  const payload = decodeJwtPayload(token);
  if (!payload || !payload.exp) return <Navigate to="/login" replace state={{ from: loc }} />;

  const now = Math.floor(Date.now() / 1000);
  if (payload.exp <= now) return <Navigate to="/login" replace state={{ from: loc }} />;

  return children;
}
