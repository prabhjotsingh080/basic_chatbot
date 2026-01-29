import React, { useState, useEffect } from 'react';
import "./Separtion.css";

function Separtion({ onResize }) {
  const [isResizing, setIsResizing] = useState(false);

  const startResizing = () => setIsResizing(true);
  const stopResizing = () => setIsResizing(false);

  const resize = (e) => {
    if (isResizing) {
      // Pass the new width (mouse X position) back to the parent
      onResize(e.clientX);
    }
  };

  useEffect(() => {
    window.addEventListener("mousemove", resize);
    window.addEventListener("mouseup", stopResizing);
    return () => {
      window.removeEventListener("mousemove", resize);
      window.removeEventListener("mouseup", stopResizing);
    };
  }, [isResizing]);

  return (
    <div 
      className={`separtion ${isResizing ? "resizing" : ""}`} 
      onMouseDown={startResizing}
    />
  );
}

export default Separtion;