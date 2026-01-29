import React, { useEffect, useState } from 'react'
import { FiSun } from "react-icons/fi";
import { IoMoonOutline } from "react-icons/io5";
import "./Darkmode.css"
function Darkmode() {
    const[mode,setmode]=useState("darkmode")
    function toggle(){
        if(mode=="darkmode"){
            setmode("lightmode")
        }else{
            setmode("darkmode")
        }
    }
    useEffect(()=>{
        document.body.className=mode
    },[mode])
  return (
    <div>
      <button className='darkmodebtn' onClick={()=>{
        toggle()
      }}>{mode==="darkmode"?<FiSun />:<IoMoonOutline />}
</button>
    </div>
  )
}

export default Darkmode
