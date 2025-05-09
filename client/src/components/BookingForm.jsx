import React, { useState, useEffect } from 'react';

const BookingForm = ({
  initialData = {},
  users = [],
  services = [],
  onSubmit,
  onCancel
}) => {
  const [form, setForm] = useState({
    user_id: '',
    service_id: '',
    scheduled_for: '',
    status: 'pending',
    notes: '',
    ...initialData
  });

  // Pre-fill datetime-local when editing
  useEffect(() => {
    if (initialData.scheduled_for) {
      const dt = new Date(initialData.scheduled_for);
      setForm(f => ({
        ...f,
        scheduled_for: dt.toISOString().slice(0,16)
      }));
    }
  }, [initialData.scheduled_for]);

  const handleChange = e => {
    const { name, value } = e.target;
    setForm(f => ({ ...f, [name]: value }));
  };

  const handleSubmit = e => {
    e.preventDefault();
    onSubmit({
      ...form,
      scheduled_for: new Date(form.scheduled_for).toISOString()
    });
  };

  return (
    <form onSubmit={handleSubmit} style={{ marginBottom: 20 }}>
      <select
        name="user_id"
        value={form.user_id}
        onChange={handleChange}
        required
      >
        <option value="">— Select User —</option>
        {users.map(u => (
          <option key={u.id} value={u.id}>
            {u.email} ({u.username})
          </option>
        ))}
      </select>

      <select
        name="service_id"
        value={form.service_id}
        onChange={handleChange}
        required
      >
        <option value="">— Select Service —</option>
        {services.map(s => (
          <option key={s.id} value={s.id}>
            {s.name}
          </option>
        ))}
      </select>

      <input
        type="datetime-local"
        name="scheduled_for"
        value={form.scheduled_for}
        onChange={handleChange}
        required
        style={{ marginLeft: 8 }}
      />

      <select
        name="status"
        value={form.status}
        onChange={handleChange}
        style={{ marginLeft: 8 }}
      >
        {['pending','confirmed','completed','cancelled'].map(st => (
          <option key={st} value={st}>{st}</option>
        ))}
      </select>

      <input
        type="text"
        name="notes"
        placeholder="Notes"
        value={form.notes}
        onChange={handleChange}
        style={{ marginLeft: 8 }}
      />

      <button type="submit" style={{ marginLeft: 8 }}>
        {initialData.id ? 'Save' : 'Create'}
      </button>
      {initialData.id && (
        <button
          type="button"
          onClick={onCancel}
          style={{ marginLeft: 4 }}
        >
          Cancel
        </button>
      )}
    </form>
  );
};

export default BookingForm;
