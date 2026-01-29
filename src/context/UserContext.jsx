import React, { createContext, useState } from "react";
export const dataContext = createContext();
import run from "../Gemini";
function UserContext({ children }) {
  const [input, setinput] = useState("");
  const[showResult,setShowResult]=useState(false)
const[loading,setLoading]=useState(false)
const[resultData,setResultData]=useState("")
const[recentPrompt,setRecentPrompt]=useState("")
const[prevPrompt,setPrevPrompt]=useState([])
function newchat(){
  setShowResult(false)
  setLoading(false)
}
  async function sent(input) {
setResultData("")
    setShowResult(true)
    setRecentPrompt(input)
    setLoading(true)
    setPrevPrompt(prev=>[...prev,input])
   let response= await run(input);
   setResultData(response.split("**")&&response.split("*"))
   setLoading(false)
       setinput("")
  }
  const data = {
    input,
    setinput,
    sent,
    loading,
    setLoading,
    showResult,
    setShowResult,
    resultData,
    setResultData,recentPrompt,setRecentPrompt,
    prevPrompt,newchat
  };
  return (
    <>
      <dataContext.Provider value={data}>{children}</dataContext.Provider>
    </>
  );
}

export default UserContext;
