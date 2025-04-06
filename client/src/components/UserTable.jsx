import React from 'react';

const UserTable = ({ users }) => {
  return (
    <table style={{ width: '100%', borderCollapse: 'collapse' }}>
      <thead>
        <tr style={{ background: '#f4f4f4' }}>
          <th style={cell}>Email</th>
          <th style={cell}>Username</th>
          <th style={cell}>Role</th>
          <th style={cell}>Last Login</th>
        </tr>
      </thead>
      <tbody>
        {users.map(user => (
          <tr key={user.id} style={{ borderBottom: '1px solid #ddd' }}>
            <td style={cell}>{user.email}</td>
            <td style={cell}>{user.username}</td>
            <td style={cell}>{user.role}</td>
            <td style={cell}>{user.last_login ? new Date(user.last_login).toLocaleString() : 'Never'}</td>
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
