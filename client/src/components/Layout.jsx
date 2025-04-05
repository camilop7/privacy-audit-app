import React from 'react';
import Sidebar from './Sidebar';

const Layout = ({ children }) => {
  return (
    <div>
      <Sidebar />
      <div style={{
        marginLeft: '240px',
        padding: '20px',
        transition: 'margin-left 0.3s',
      }}>
        {children}
      </div>
    </div>
  );
};

export default Layout;
