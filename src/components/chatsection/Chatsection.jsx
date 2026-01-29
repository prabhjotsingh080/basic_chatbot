import React, { useContext } from 'react'
import "./Chatsection.css"
import { LuSendHorizontal } from "react-icons/lu";

import Darkmode from '../darkmode/Darkmode'
import { dataContext } from '../../context/UserContext';
import user from "../../assets/user.png";

import ai from "../../assets/ai.png";

function Chatsection() {
  let{sent,input,setinput,showResult,resultData,recentPrompt,loading}=useContext(dataContext)
  return (
    <div className='chatsection'>
    <div className="topsection">
      {!showResult? <div className="headings">
            <span>HELLO USER</span><span >I'm Your Own Assistant</span>
            <span>How can i help You...?</span>
        </div>:<div className="result">
        <div className="userbox"> 
          <img src={user} alt="" width="60px"/>
          <p>{recentPrompt}</p>

          </div>
          <div className="aibox">
            <img src={ai} alt="" width="60px"/>
            {loading?<div className='loader'>
              <hr />
              <hr />
              <hr />
            </div>:<p></p>}
            <p>{resultData}</p>
          </div>
           </div>}
       
    </div>
    <div className="bottomsection">
      <input type="text" onChange={(e)=>setinput(e.target.value)} placeholder='enter a prompt'  value={input}/>
{input?<button id='sendbtn' onClick={()=>{sent(input)}}>
      <LuSendHorizontal /></button>:null}

      <Darkmode/>
    </div>
    </div>
  )
}

export default Chatsection
