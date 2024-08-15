import React from 'react'

import Sidabar from '../components/Sidabar'
import Task_form from '../components/Task_Form'
import { Route, Routes, Navigate } from 'react-router-dom';
import Task from '../pages/Create_task'
import Todos from '../pages/Todos'
import Issues from '../pages/Issues'
import Features from '../pages/Features'
import Profile from '../pages/Profile'
import Dashboard from '../pages/Dashboard'



const Admin_homepage = () => {
  return (
    <>
    

    <div className="flex">
      <div className="">
     <Sidabar />
    

      </div>

      <div className="">
     
          <Routes>
          <Route path="/" element={<Navigate to="/admin/dashboard" />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path='/task' element = {<Task />}></Route>
            <Route path='/todos' element = {<Todos />}></Route>
            <Route path='/issues' element = {<Issues />}></Route>
            <Route path='/features' element = {<Features />}></Route>
            <Route path='/profile' element = {<Profile />}></Route>
          </Routes>
      </div>
    </div>


    </>
  )
}

export default Admin_homepage
