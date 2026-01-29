import React, { useState, useEffect, useCallback } from 'react';
import "./Separtion.css"; // Keep this as is for now so your CSS doesn't break!

function Separation({ onResize }) {
  const [isResizing, setIsResizing] = useState(false);

  const startResizing = () => setIsResizing(true);
  const stopResizing = () => setIsResizing(false);

  // Using useCallback ensures the function isn't recreated on every render
  const resize = useCallback((e) => {
    if (isResizing) {
      onResize(e.clientX);
    }
  }, [isResizing, onResize]);

  useEffect(() => {
    if (isResizing) {
      window.addEventListener("mousemove", resize);
      window.addEventListener("mouseup", stopResizing);
    }

    return () => {
      window.removeEventListener("mousemove", resize);
      window.removeEventListener("mouseup", stopResizing);
    };
  }, [isResizing, resize]);

  return (
    <div 
      className={`separtion ${isResizing ? "resizing" : ""}`} 
      onMouseDown={startResizing}
    />
  );
}

export default Separation;