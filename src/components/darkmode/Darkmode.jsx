import React, { useEffect, useState } from 'react';
import { FiSun } from "react-icons/fi";
import { IoMoonOutline } from "react-icons/io5";
import "./Darkmode.css";

function Darkmode() {
    // Initializing state with localStorage to persist user choice
    const [mode, setmode] = useState(() => localStorage.getItem("theme") || "darkmode");

    function toggle() {
        setmode((prevMode) => (prevMode === "darkmode" ? "lightmode" : "darkmode"));
    }

    useEffect(() => {
        document.body.className = mode;
        localStorage.setItem("theme", mode); // Save preference
    }, [mode]);

    return (
        <div>
            <button 
                className='darkmodebtn' 
                onClick={toggle} 
                aria-label="Toggle dark mode"
            >
                {mode === "darkmode" ? <FiSun /> : <IoMoonOutline />}
            </button>
        </div>
    );
}

export default Darkmode;