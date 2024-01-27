import React from 'react'
import axios from 'axios'
import { useState } from 'react'
import { useNavigate } from 'react-router-dom';

const Contact = () => {
  const [Form, setForm] = useState({
    name: "",
    email: "",
    message: ""
  });
  const [loading, setLoading] = useState(false);
  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm({...Form, [name]: value})
  }

  const handleSubmit = (e) => {
    e.preventDefault();
    setLoading(true);

    emailjs.send(
      `${import.meta.env.VITE_SERVICE_ID}`,
      `${import.meta.env.VITE_TEMPLATE_ID}`,
      {
        from_name: form.name,
        to_name: 'Bilal',
        from_email: form.email,
        to_email: 'imbilal164@gmail.com',
        message: form.message,
      },
      `${import.meta.env.VITE_PUBLIC_KEY}`
    )
    .then(() => {
      setLoading(false);
      alert('Thank You. We will get back to you as soon as possible');

      setForm({
        name: '',
        email: '',
        message: '',
      })
    }, (error) => {
      setLoading(false);
      console.log(error);
      alert("Something went wrong");
    })
  } 
  return (
    <div className='bg-heroBG bg-cover'>
      <div className=' flex items-start justify-start sm:m-auto m-[50px]'>
        <div className=' container bg-gradient-to-b from-[#6F61C0] from-10% via-[#3c3661] h-auto to-slate-900  sm:w-[800px] w-[400px] sm:mb-[200px] sm:mt-[90px] rounded-3xl mx-auto'>
          <p className=' mx-20 mt-8 font-mono text-[30px] text-white uppercase'>Get in Touch</p><br />
          <h1 className='mx-20 font-bold text-7xl text-black tracking-wide mt-[-23px]'>Contact.</h1>

          <form onSubmit={handleSubmit} className='mt-12 flex flex-col gap-8'>
          <label className='flex flex-col'>
            <span className='text-white font-medium mb-4 mx-8'>Your Name</span>
            <input 
              type='text'
              name='name'
              value={Form.name}
              onChange={handleChange}
              placeholder="What's your name?"
              className='bg-[#6F61C0] py-4 px-6 mx-8 placeholder:text-lg text-white rounded-lg outlined-none border-none font-medium'
            />
          </label>
          <label className='flex flex-col'>
            <span className='text-white font-medium mb-4 mx-8'>Your Email</span>
            <input 
              type='text'
              name='email'
              value={Form.email}
              onChange={handleChange}
              placeholder="Enter your email"
              className='bg-[#6F61C0] mx-8 py-4 px-6 placeholder:text-lg text-white rounded-lg outlined-none border-none font-medium'

            />
          </label>
          <label className='flex flex-col'>
            <span className='text-white font-medium mb-4 mx-8'>Your Message</span>
            <textarea
              rows='7'
              name='message'
              value={Form.message}
              onChange={handleChange}
              placeholder="Leave your message"
              className='bg-[#6F61C0] mx-8 py-4 px-6 placeholder:text-secondary text-white rounded-lg outlined-none border-none font-medium'

            />
          </label>
          <button type="submit" 
            className='bg-[#6F61C0] mx-8 my-4 py-3 px-8 rounded-xl outline-none w-fit text-white font-bold shadow-md shadow-[#000000]'

          >
            {loading? "Sending..." : "Send"}
          </button>
          </form>
        </div>
      </div>
    </div>
  )
}

export default Contact