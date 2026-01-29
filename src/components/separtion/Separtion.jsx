import React, { useState, useEffect } from 'react';
import "./Separtion.css";

function Separtion({ onResize }) {
  const [isReseizeing, setIsResizing] = useState(false);

  const startResizing = () => setIsResizing(true);
  const stopResizing = () => setIsResizing(false);

  const resize = (e) => {
    if (isReseizeing) {
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
  }, [isReseizing]);

  return (
    <div 
      className={`separtion ${isReseizing ? "resizing" : ""}`} 
      onMouseDown={startResizing}
    />
  );
}

export default Separtion;