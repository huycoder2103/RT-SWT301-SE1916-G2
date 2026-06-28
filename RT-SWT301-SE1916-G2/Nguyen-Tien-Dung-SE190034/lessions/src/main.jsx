import { createRoot } from 'react-dom/client';
import App from './App.jsx';
import './styles/base.css';
import './styles/app.css';

try { const t = localStorage.getItem('lessions-theme'); if (t) document.documentElement.setAttribute('data-theme', t); } catch (e) {}

createRoot(document.getElementById('root')).render(<App />);
