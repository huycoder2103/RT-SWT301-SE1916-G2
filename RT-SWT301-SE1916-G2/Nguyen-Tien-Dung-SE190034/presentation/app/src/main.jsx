import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.jsx';
import './styles/deck.css';
import './styles/app.css';

// restore theme before paint
try { const t = localStorage.getItem('deck-theme'); if (t) document.documentElement.setAttribute('data-theme', t); } catch (e) {}

createRoot(document.getElementById('root')).render(<App />);
