import React, { useState } from 'react';
import Header from './Header';
import DrawingApp from './DrawingApp';
import About from './About';
import { Routes, Route } from 'react-router-dom';

const App = () => {
  const [darkMode, setDarkMode] = useState(false);

  return (
    <div>
      <Header darkMode={darkMode} setDarkMode={setDarkMode} />
      <Routes>
        <Route path="/" element={<DrawingApp />} />
        <Route path="/about" element={<About darkMode={darkMode} />} />
      </Routes>
    </div>
  );
};

export default App;
