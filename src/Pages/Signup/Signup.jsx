import React from 'react'
import axios from 'axios'
import { useState } from 'react'
function Signup() {
    const [uname, setUname] = useState("");
    const [psw, setPsw] = useState("");
    const [cpsw, setCpsw] = useState("");
    const [name, setName] = useState("");
    const [age, setAge] = useState("");
    const [mobile, setMobile] = useState("");
    const [email, setEmail] = useState("");

    let submit=async(e)=>{
    e.preventDefault()

    await axios.post('',{
        uname:uname,
        password1:psw,
        password2:cpsw,
        name:name,
        age:age,
        mobile:mobile,
        email:email
        })
        .then(res=>{
        console.log(res)
        }
        )
        .catch(err=>{
            console.log(err)
        })
    }

  return (
    <div className="container  w-80 mx-auto my-20 px-6 py-6 shadow ">
        <h1 className="text-purple-600 font-bold font-sans text-4xl text-center">
          Login
        </h1>
        <div className="h-0.5 bg-gray-200 w-36 mx-auto mt-2.5"></div>
        <form action="" method="POST" onSubmit={submit}>
          <div className="flex flex-col my-5">
            <label className="my-2 text-xl font-medium" for="uname">
              Username
            </label>
            <input
              type="text"
              id="uname"
              name="uname"
              value={uname}
              required: true
              className="mt-1 mb-3 shadow-md border-none focus:ring-transparent rounded-sm bg-gray-100 text-black-500"
              onChange={(e) => setUname(e.target.value)}
            />
            <label className="my-2 text-xl font-medium" for="psw">
              Password
            </label>
            <input
              type="password"
              id="psw"
              name="psw"
              value={psw}
              required: true
              className="mt-1 mb-3 shadow-md border-none focus:ring-transparent rounded-sm bg-gray-100 text-black-500"
              onChange={(e) => setPsw(e.target.value)}
            />
            <label className="my-2 text-xl font-medium" for="psw">
              Confirm Password
            </label>
            <input
              type="password"
              id="cpsw"
              name="cpsw"
              value={cpsw}
              required: true
              className="mt-1 mb-3 shadow-md border-none focus:ring-transparent rounded-sm bg-gray-100 text-black-500"
              onChange={(e) => setCpsw(e.target.value)}
            />
            <label className="my-2 text-xl font-medium" for="psw">
              Name
            </label>
            <input
              type="text"
              id="name"
              name="name"
              value={name}
              required: true
              placeholder='Should be unique'
              className="mt-1 mb-3 shadow-md border-none focus:ring-transparent rounded-sm bg-gray-100 text-black-500"
              onChange={(e) => setName(e.target.value)}
            />
            <label className="my-2 text-xl font-medium" for="psw">
              Age
            </label>
            <input
              type="number"
              id="age"
              name="age"
              value={age}
              className="mt-1 mb-3 shadow-md border-none focus:ring-transparent rounded-sm bg-gray-100 text-black-500"
              onChange={(e) => setAge(e.target.value)}
            />
            <label className="my-2 text-xl font-medium" for="psw">
              Mobile Number
            </label>
            <input
              type="number"
              id="mobile"
              name="mobile"
                value={mobile}
              className="mt-1 mb-3 shadow-md border-none focus:ring-transparent rounded-sm bg-gray-100 text-black-500"
              onChange={(e) => setMobile(e.target.value)}
            />
            <label className="my-2 text-xl font-medium" for="psw">
              email
            </label>
            <input
              type="email"
              id="email"
              name="email"
                value={email}
              required: true
              className="mt-1 mb-3 shadow-md border-none focus:ring-transparent rounded-sm bg-gray-100 text-black-500"
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          <div className="text-center mt-3">
            
            <button className="px-7 py-2 mx-2 font-semibold text-white bg-purple-600 rounded ">
              Submit
            </button>
          </div>
        </form>
        
      </div>
  )
}

export default Signup