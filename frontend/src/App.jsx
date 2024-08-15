import './App.css'
import {  Route, Routes } from "react-router-dom" 
import Login from './pages/Login'
import Admin_homepage from './pages/Admin_homepage'


function App() {
 

  return (
  
    <Routes>
      <Route path="/"  element = {<Login  />}   />
      <Route path="/admin/*"  element = {<Admin_homepage  />}   />
    </Routes>

    
  
  )
}

export default App
