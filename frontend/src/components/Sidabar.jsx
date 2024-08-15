import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import { BiSidebar } from "react-icons/bi";

const Sidebar = () => {
  // State to manage visibility of sidebar
  const [isSidebarVisible, setSidebarVisible] = useState(true);

  // Function to toggle sidebar visibility
  const toggleSidebar = () => {
    setSidebarVisible(!isSidebarVisible);
  };

  return (
    <section
      className={`bg-[#FBFAFF] h-[100vh] ${
        isSidebarVisible ? 'w-[200px]' : 'w-[60px]'
      } flex flex-col justify-between transition-all duration-300 ease-in-out relative`}
    >
      {/* Sidebar Header */}
      <div className="flex items-center justify-between p-4">
        {/* Title - Only visible when sidebar is expanded */}
        {isSidebarVisible && (
          <h1
            className="text-lg font-bold transition-opacity duration-300 ease-in-out"
          >
            Hi Abdirsak
          </h1>
        )}
        {/* Icon - Always visible and fixed position */}
        <div className="absolute top-4 right-4">
          <BiSidebar 
            onClick={toggleSidebar} 
            className="cursor-pointer text-2xl" 
          />
        </div>
      </div>

      {/* Navigation Links - Conditionally Rendered */}
      <div
        className={`flex-grow space-y-4 mt-4 transition-opacity duration-300 ease-in-out ${
          isSidebarVisible ? 'opacity-100' : 'opacity-0'
        }`}
      >
        {isSidebarVisible && (
          <nav className='ml-2'>
            <ul className="space-y-4">
              <li className="py-2">
                <NavLink
                  to="/admin/dashboard"
                  className={({ isActive }) =>
                    isActive
                      ? 'text-white bg-[#1EA7FF] px-3 py-2 rounded-md'
                      : 'text-gray-700 px-3 py-2 rounded-md'
                  }
                >
                  Dashboard
                </NavLink>
              </li>
              <li className="py-2">
                <NavLink
                  to="/admin/task"
                  className={({ isActive }) =>
                    isActive
                      ? 'text-white bg-[#1EA7FF] px-3 py-2 rounded-md'
                      : 'text-gray-700 px-3 py-2 rounded-md'
                  }
                >
                  Task
                </NavLink>
              </li>
              <li className="py-2">
                <NavLink
                  to="/admin/todos"
                  className={({ isActive }) =>
                    isActive
                      ? 'text-white bg-[#1EA7FF] px-3 py-2 rounded-md'
                      : 'text-gray-700 px-3 py-2 rounded-md'
                  }
                >
                  Todos
                </NavLink>
              </li>
              <li className="py-2">
                <NavLink
                  to="/admin/issues"
                  className={({ isActive }) =>
                    isActive
                      ? 'text-white bg-[#1EA7FF] px-3 py-2 rounded-md'
                      : 'text-gray-700 px-3 py-2 rounded-md'
                  }
                >
                  Issues
                </NavLink>
              </li>
              <li className="py-2">
                <NavLink
                  to="/admin/features"
                  className={({ isActive }) =>
                    isActive
                      ? 'text-white bg-[#1EA7FF] px-3 py-2 rounded-md'
                      : 'text-gray-700 px-3 py-2 rounded-md'
                  }
                >
                  Features
                </NavLink>
              </li>
            </ul>
          </nav>
        )}
      </div>

      {/* Bottom Profile Link - Conditionally Rendered */}
      {isSidebarVisible && (
        <div className="mt-4 p-4">
          <NavLink
            to="/admin/profile"
            className="bg-[#1EA7FF] text-white px-[60px] py-2 rounded-md text-center"
          >
            Profile
          </NavLink>
        </div>
      )}
    </section>
  );
};

export default Sidebar;
