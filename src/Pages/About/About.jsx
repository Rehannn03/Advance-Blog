import React from 'react'
import { useNavigate } from 'react-router-dom'
function About() {
    const navigate=useNavigate()

    const goToHome=()=>{
        navigate('/login')
    }
  return (
    <div className='justify-center'>
        <h1 className='text-center text-3xl py-5 '>
            ABOUT
        </h1>
        <button className='' onClick={goToHome}>
            Go to Home
        </button>
    </div>
  )
}

export default About