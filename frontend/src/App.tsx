import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { TableProvider } from "./contexts/TableContext";
import Employee from "./pages/Employee";
import Manager from "./pages/Manager";
import Timeoffrequest from "./pages/Timeoffrequest";

function App() {
  return (
    <TableProvider>
      <div className="app-container">
        <main className="app-main">
          <Routes>
            <Route path="/employee" element={<Employee />} />
            <Route path="/manager" element={<Manager />} />
            <Route path="/timeoffrequest" element={<Timeoffrequest />} />
            <Route path="/" element={<Navigate to="/employee" replace />} />
            <Route path="*" element={<Navigate to="/employee" replace />} />
          </Routes>
        </main>
      </div>
    </TableProvider>
  );
}
export default App;
