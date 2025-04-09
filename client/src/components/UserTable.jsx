import React from 'react';

const UserTable = ({ users, onToggleStatus }) => {
  return (
    <table style={{
      width: '100%',
      borderCollapse: 'collapse',
      background: '#fff',
      boxShadow: '0 0 10px rgba(0,0,0,0.1)'
    }}>
      <thead style={{ background: '#1a1a1a', color: '#fff' }}>
        <tr>
          <th style={cell}>Username</th>
          <th style={cell}>Email</th>
          <th style={cell}>Role</th>
          <th style={cell}>Status</th>
          <th style={cell}>Actions</th>
        </tr>
      </thead>
      <tbody>
        {users.map(user => (
          <tr key={user.id} style={{ borderBottom: '1px solid #eee' }}>
            <td style={cell}>{user.username}</td>
            <td style={cell}>{user.email}</td>
            <td style={cell}>{user.role}</td>
            <td style={{
              ...cell,
              fontWeight: 'bold',
              color: user.is_active ? 'green' : 'red'
            }}>
              {user.is_active ? 'Active' : 'Banned'}
            </td>
            <td style={cell}>
              <button
                onClick={() => onToggleStatus(user.id)}
                style={{
                  padding: '6px 12px',
                  background: user.is_active ? '#e74c3c' : '#2ecc71',
                  color: '#fff',
                  border: 'none',
                  borderRadius: '5px',
                  cursor: 'pointer'
                }}
              >
                {user.is_active ? 'Ban' : 'Unban'}
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

const cell = {
  padding: '12px',
  textAlign: 'left'
};

export default UserTable;
