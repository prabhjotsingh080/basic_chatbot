import React, { useContext } from 'react'
import Sidebar from './components/sidebar/Sidebar'
import Chatsection from './components/chatsection/Chatsection'
import Separtion from './components/separtion/Separtion'
import { dataContext } from './context/UserContext'


function App() {
  let data=useContext(dataContext)
  return (
    <>
   <Sidebar/>
   <Separtion/>
   <Chatsection/>
    
    </>
  )
}

export default App
