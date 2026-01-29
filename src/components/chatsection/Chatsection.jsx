import React, { useContext } from 'react';
import "./Chatsection.css";
import { LuSendHorizontal } from "react-icons/lu";

import Darkmode from '../darkmode/Darkmode';
import { dataContext } from '../../context/UserContext';
import user from "../../assets/user.png";
import ai from "../../assets/ai.png";

function Chatsection() {
  const { sent, input, setinput, showResult, resultData, recentPrompt, loading } = useContext(dataContext);

  // Helper to trigger send on 'Enter' key press
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && input.trim()) {
      sent(input);
    }
  };

  return (
    <div className='chatsection'>
      <div className="topsection">
        {!showResult ? (
          <div className="headings">
            <span>HELLO USER</span>
            <span>I'm Your Own Assistant</span>
            <span>How can I help You...?</span>
          </div>
        ) : (
          <div className="result">
            <div className="userbox">
              <img src={user} alt="User Icon" width="60px" />
              <p>{recentPrompt}</p>
            </div>
            
            <div className="aibox">
              <img src={ai} alt="AI Icon" width="60px" />
              {loading ? (
                <div className='loader'>
                  <hr /><hr /><hr />
                </div>
              ) : (
                <p dangerouslySetInnerHTML={{ __html: resultData }}></p> 
                /* Note: Using dangerouslySetInnerHTML if resultData contains HTML/formatting */
              )}
            </div>
          </div>
        )}
      </div>

      <div className="bottomsection">
        <div className="input-wrapper">
          <input 
            type="text" 
            onChange={(e) => setinput(e.target.value)} 
            onKeyDown={handleKeyDown}
            placeholder='Enter a prompt'  
            value={input} 
          />
          {input.trim() ? (
            <button 
              id='sendbtn' 
              onClick={() => sent(input)}
              aria-label="Send message"
            >
              <LuSendHorizontal />
            </button>
          ) : null}
        </div>
        <Darkmode />
      </div>
    </div>
  );
}

export default Chatsection;