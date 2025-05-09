import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import BookingTable from '../components/BookingTable';
import BookingForm from '../components/BookingForm';

const BookingsDashboard = () => {
  const [bookings, setBookings] = useState([]);
  const [users, setUsers] = useState([]);
  const [services, setServices] = useState([]);
  const [editing, setEditing] = useState(null);
  const [loading, setLoading] = useState(false);

  const getAuthHeaders = () => {
    const token = localStorage.getItem('token');
    return { Authorization: `Bearer ${token}` };
  };

  const loadData = useCallback(async () => {
    setLoading(true);
    try {
      const [bkRes, userRes, svcRes] = await Promise.all([
        axios.get('http://localhost:8000/api/bookings', {
          headers: getAuthHeaders(),
        }),
        axios.get('http://localhost:8000/api/admin/users', {
          headers: getAuthHeaders(),
        }),
        axios.get('http://localhost:8000/api/services', {
          headers: getAuthHeaders(),
        }),
      ]);
      setBookings(bkRes.data);
      setUsers(userRes.data);
      setServices(svcRes.data);
    } catch (err) {
      console.error('❌ Failed to load data', err.response?.data || err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const handleCreate = async data => {
    try {
      await axios.post(
        'http://localhost:8000/api/bookings',
        data,
        { headers: getAuthHeaders() }
      );
      loadData();
    } catch (err) {
      console.error('❌ Create failed', err.response?.data || err.message);
    }
  };

  const handleUpdate = async data => {
    try {
      await axios.put(
        `http://localhost:8000/api/bookings/${editing.id}`,
        data,
        { headers: getAuthHeaders() }
      );
      setEditing(null);
      loadData();
    } catch (err) {
      console.error('❌ Update failed', err.response?.data || err.message);
    }
  };

  const handleDelete = async id => {
    if (!window.confirm('Delete this booking?')) return;
    try {
      await axios.delete(
        `http://localhost:8000/api/bookings/${id}`,
        { headers: getAuthHeaders() }
      );
      loadData();
    } catch (err) {
      console.error('❌ Delete failed', err.response?.data || err.message);
    }
  };

  const handleEditClick = bk => {
    setEditing(bk);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>📅 Bookings Management</h2>

      {loading ? (
        <p>Loading…</p>
      ) : (
        <>
          <BookingForm
            key={editing ? editing.id : 'new'}
            initialData={editing || {}}
            users={users}
            services={services}
            onSubmit={editing ? handleUpdate : handleCreate}
            onCancel={() => setEditing(null)}
          />

          <BookingTable
            bookings={bookings}
            onEdit={handleEditClick}
            onDelete={handleDelete}
          />
        </>
      )}
    </div>
  );
};

export default BookingsDashboard;
