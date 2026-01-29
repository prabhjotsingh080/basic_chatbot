import React, { useState, useEffect, useCallback } from 'react';
import "./Separtion.css"; 

function Separtion({ onResize }) {
  const [isReseizeing, setIsResizing] = useState(false);

  const startResizing = () => setIsResizing(true);
  const stopResizing = () => setIsResizing(false);

  const resize = (e) => {
    if (isReseizeing) {
    
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
  }, [isReseizing]);

  return (
    <div 
      className={`separtion ${isReseizing ? "resizing" : ""}`} 
      onMouseDown={startResizing}
    />
  );
}

export default Separation;