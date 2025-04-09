import React, { useEffect, useState } from 'react';
import axios from 'axios';
import UserTable from '../components/UserTable';

const AdminDashboard = () => {
  const [users, setUsers] = useState([]);
  const [roleFilter, setRoleFilter] = useState('');
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(false);

  // Form state for new user
  const [newUser, setNewUser] = useState({
    email: '',
    username: '',
    hashed_password: '',
    role: 'user'
  });

  const roles = ['admin', 'analyst', 'user'];

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const res = await axios.get('http://localhost:8000/api/admin/users');
      console.log('✅ Users fetched:', res.data);
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
      setUsers(prev =>
        prev.map(user =>
          user.id === userId ? { ...user, is_active: !user.is_active } : user
        )
      );
    } catch (err) {
      console.error('❌ Failed to toggle user status', err);
    }
  };

  const createUser = async () => {
    try {
      await axios.post('http://localhost:8000/api/admin/users', newUser);
      setNewUser({ email: '', username: '', hashed_password: '', role: 'user' });
      fetchUsers();
    } catch (err) {
      console.error('❌ Failed to create user', err);
    }
  };

  const deleteUser = async (userId) => {
    try {
      await axios.delete(`http://localhost:8000/api/admin/users/${userId}`);
      fetchUsers();
    } catch (err) {
      console.error('❌ Failed to delete user', err);
    }
  };

  const filteredUsers = users.filter(user =>
    (!roleFilter || user.role === roleFilter) &&
    (user.email.toLowerCase().includes(search.toLowerCase()) ||
     user.username.toLowerCase().includes(search.toLowerCase()))
  );

  return (
    <div style={{ padding: '20px' }}>
      <h2>🔐 Admin Dashboard</h2>

      {/* Search & Filter */}
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

      {/* New User Form */}
      <div style={{ marginBottom: '30px', borderTop: '1px solid #ddd', paddingTop: '20px' }}>
        <h4>Create New User</h4>
        <input
          placeholder="Email"
          value={newUser.email}
          onChange={(e) => setNewUser({ ...newUser, email: e.target.value })}
          style={{ marginRight: '10px', padding: '6px' }}
        />
        <input
          placeholder="Username"
          value={newUser.username}
          onChange={(e) => setNewUser({ ...newUser, username: e.target.value })}
          style={{ marginRight: '10px', padding: '6px' }}
        />
        <input
          type="password"
          placeholder="Password"
          value={newUser.hashed_password}
          onChange={(e) => setNewUser({ ...newUser, hashed_password: e.target.value })}
          style={{ marginRight: '10px', padding: '6px' }}
        />
        <select
          value={newUser.role}
          onChange={(e) => setNewUser({ ...newUser, role: e.target.value })}
          style={{ marginRight: '10px', padding: '6px' }}
        >
          {roles.map(role => (
            <option key={role} value={role}>{role}</option>
          ))}
        </select>
        <button onClick={createUser} style={{ padding: '6px 12px' }}>
          ➕ Create User
        </button>
      </div>

      {/* User Table */}
      {loading ? (
        <p>Loading users...</p>
      ) : (
        <UserTable
          users={filteredUsers}
          onToggleStatus={toggleUserStatus}
          onDelete={deleteUser}
        />
      )}
    </div>
  );
};

export default AdminDashboard;
