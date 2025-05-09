import React from 'react';

const BookingTable = ({ bookings, onEdit, onDelete }) => (
  <table border="1" cellPadding="8" style={{ width: '100%', marginTop: 20 }}>
    <thead>
      <tr>
        <th>User</th>
        <th>Service</th>
        <th>Scheduled For</th>
        <th>Status</th>
        <th>Notes</th>
        <th>Actions</th>
      </tr>
    </thead>
    <tbody>
      {bookings.map(bk => (
        <tr key={bk.id}>
          <td>{bk.user_id}</td>
          <td>{bk.service.name}</td>
          <td>{new Date(bk.scheduled_for).toLocaleString()}</td>
          <td>{bk.status}</td>
          <td>{bk.notes || '—'}</td>
          <td>
            <button onClick={() => onEdit(bk)}>✏️</button>
            <button onClick={() => onDelete(bk.id)}>🗑️</button>
          </td>
        </tr>
      ))}
    </tbody>
  </table>
);

export default BookingTable;
