import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

 const handleLogin = async (e) => {
  e.preventDefault();
  setError('');
  try {
    const res = await axios.post('http://localhost:8000/api/auth/login', { email, password });
    localStorage.setItem('token', res.data.access_token);
    navigate('/scan');    // choose any protected route
  } catch (err) {
    setError('Invalid credentials');
  }
};

  return (
    <div style={{ padding: '40px', maxWidth: '400px', margin: 'auto' }}>
      <h2>🔐 Login</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={handleLogin}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          required
          onChange={(e) => setEmail(e.target.value)}
          style={{ width: '100%', padding: '10px', marginBottom: '10px' }}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          required
          onChange={(e) => setPassword(e.target.value)}
          style={{ width: '100%', padding: '10px', marginBottom: '20px' }}
        />
        <button type="submit" style={{
          padding: '10px 20px',
          backgroundColor: '#1a1a1a',
          color: 'white',
          border: 'none',
          width: '100%',
          cursor: 'pointer'
        }}>
          Log In
        </button>
      </form>
    </div>
  );
};

export default Login;
