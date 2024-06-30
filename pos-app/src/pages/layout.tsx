import React from "react";

const Layout: React.FC = ({ children }) => {
  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-blue-600 text-white p-4">POSシステム</header>
      <main className="flex flex-col items-center justify-center p-6">{children}</main>
      <footer className="bg-blue-600 text-white p-4 text-center">&copy; 2024 POS System</footer>
    </div>
  );
};

export default Layout;
