import axios from "axios";
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
export const Login = () => {
  const [uname, setUname] = useState("");
  const [psw, setPsw] = useState("");
  const [login, setLogin] = useState(false);
  let submit = async (e) => {
    e.preventDefault();
    let formData = new FormData();
    formData.append("uname", uname);
    formData.append("password", psw);
    const navigate=useNavigate()
    try {
      const response = await fetch(
        "https://4415-103-220-42-156.ngrok-free.app/login",
        {
          method: "POST",
          body: formData,
        }
      )
        .then((res) => res.json())
        .then((data) => {
          localStorage.setItem("token", data.access);
          console.log(data);
        })
        .catch((err) => console.log(err));
      setUname("");
      setPsw("");
      if(response.status===200){
        alert("Login Successful");
        navigate('/user/add_blog')
      }
      if(response.status===401){
        alert("Invalid Credentials")
      }
    } catch (error) {
      console.log(error.message.data);
    }
    
  };

  let forgotPassword = async (e) => {
    e.preventDefault();

    try {
      axios
        .post("", {
          uname: uname,
        })
        .then((res) => {
          console.log(res);
        });
      alert("Password Reset Successful");
      setUname("");
      setPsw("");
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <>
      <div className="container  w-80 mx-auto my-20 px-6 py-6 shadow  ">
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
              className="mt-1 mb-3 shadow-md border-none focus:ring-transparent rounded-sm bg-gray-100 text-black-500"
              onChange={(e) => setPsw(e.target.value)}
            />
          </div>
          <div className="text-center mt-3">
            <a
              href="#"
              className="text-purple-600 font-medium px-2 hover:text-purple-400 "
              onClick={forgotPassword}
            >
              Forgot Password?
            </a>
            <button className="px-7 py-2 mx-2 font-semibold text-white bg-purple-600 rounded hover:bg-purple-400">
              Submit
            </button>
          </div>
        </form>
        <div>
          <p className="text-center mt-5 font-normal">
            Don't have an account?{" "}
            <a
              href="/signup"
              className="text-purple-600 font-medium px-2 hover:text-purple-400 "
            >
              Sign Up
            </a>
          </p>
        </div>
      </div>
    </>
  );
};
