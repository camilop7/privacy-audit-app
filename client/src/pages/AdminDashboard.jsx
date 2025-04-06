import React, { useEffect, useState } from 'react';
import axios from 'axios';

const AdminDashboard = () => {
  const [users, setUsers] = useState([]);
  const [roleFilter, setRoleFilter] = useState('');
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(false);

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const res = await axios.get('http://localhost:8000/api/admin/users');
      setUsers(res.data);
    } catch (err) {
      console.error('❌ Failed to fetch users', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const toggleUserStatus = async (userId) => {
    try {
      await axios.post(`http://localhost:8000/api/admin/toggle-user/${userId}`);
      fetchUsers(); // Refresh user list
    } catch (err) {
      console.error('❌ Failed to toggle user status', err);
    }
  };

  const filteredUsers = users.filter(user =>
    (!roleFilter || user.role === roleFilter) &&
    (user.email.toLowerCase().includes(search.toLowerCase()) ||
     user.username.toLowerCase().includes(search.toLowerCase()))
  );

  const roles = ['admin', 'analyst', 'user'];

  return (
    <div style={{ padding: '20px' }}>
      <h2>🔐 Admin Dashboard</h2>

      <div style={{ marginBottom: '20px' }}>
        <input
          type="text"
          placeholder="Search by email or username"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={{ padding: '8px', width: '300px', marginRight: '10px' }}
        />

        <select
          value={roleFilter}
          onChange={(e) => setRoleFilter(e.target.value)}
          style={{ padding: '8px' }}
        >
          <option value="">All Roles</option>
          {roles.map(role => (
            <option key={role} value={role}>{role}</option>
          ))}
        </select>
      </div>

      {loading ? (
        <p>Loading users...</p>
      ) : (
        <table style={{
          width: '100%',
          borderCollapse: 'collapse',
          background: '#fff',
          boxShadow: '0 0 10px rgba(0,0,0,0.1)'
        }}>
          <thead style={{ background: '#1a1a1a', color: '#fff' }}>
            <tr>
              <th style={{ padding: '10px' }}>Username</th>
              <th style={{ padding: '10px' }}>Email</th>
              <th style={{ padding: '10px' }}>Role</th>
              <th style={{ padding: '10px' }}>Status</th>
              <th style={{ padding: '10px' }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredUsers.map(user => (
              <tr key={user.id} style={{ borderBottom: '1px solid #eee' }}>
                <td style={{ padding: '10px' }}>{user.username}</td>
                <td style={{ padding: '10px' }}>{user.email}</td>
                <td style={{ padding: '10px' }}>{user.role}</td>
                <td style={{ padding: '10px', fontWeight: 'bold', color: user.is_active ? 'green' : 'red' }}>
                  {user.is_active ? 'Active' : 'Banned'}
                </td>
                <td style={{ padding: '10px' }}>
                  <button
                    onClick={() => toggleUserStatus(user.id)}
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
      )}
    </div>
  );
};

export default AdminDashboard;
