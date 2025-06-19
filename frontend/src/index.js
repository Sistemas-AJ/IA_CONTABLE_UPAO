import React from 'react';
import ReactDOM from 'react-dom/client';
import './styles/index.css';
import App from './App';
import { MathJaxContext } from 'better-react-mathjax';

const config = {
  loader: { load: ["[tex]/ams"] },
  tex: { packages: { "[+]": ["ams"] } }
};

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <MathJaxContext config={config}>
    <App />
  </MathJaxContext>
);
