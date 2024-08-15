import React from 'react'

const Form = () => {
  return (
  <>
    <div className="flex justify-center h-[70vh] items-center">
    <div className="flex flex-col ">
      <h1 className=' text-[25px] font-thin font-mono'>Login to Diini</h1>
      <form action="" className='mt-10 flex flex-col'>
        <input className='w-[320px] h-[40px] outline-none text-[14px] pl-2 border-[1px] border-gray-200 my-4' type="text" name="" id="" placeholder='UserName ...' />
        <input className='w-[320px] h-[40px] outline-none text-[14px] pl-2 border-[1px] border-gray-200 my-4' type="text" name="" id="" placeholder='password ...' />
        <button className='bg-[#1EA7FF] text-white w-[320px] h-[30px] mt-6 rounded-md'>Login</button>
      </form>
    </div>
    </div>
  </>
  )
}

export default Form
