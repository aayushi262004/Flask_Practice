import React, { useState } from 'react';
import ReactDOM from 'react-dom/client'; // ✅ use this for React 18+
// Optional if you have styles

const App = () => {
  const [message] = useState('Hello from React!');
  return (
    <div className="app">
      {message}
    </div>
  );
};

// ✅ Create root and render
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
