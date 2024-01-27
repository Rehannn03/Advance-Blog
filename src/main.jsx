import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import { RouterProvider, createBrowserRouter, createRoutesFromElements,Route } from 'react-router-dom'
import { Login } from './Pages/Login/Login.jsx'
import Home from './Pages/Home/Home.jsx'
import Error from './components/Error/Error.jsx'
import Signup from './Pages/Signup/Signup.jsx'
import Contact from './Pages/Contact/Contact.jsx'

const router = createBrowserRouter(
  createRoutesFromElements(
    <>
    
    <Route path='/' element={<App/>} >
      <Route path='' element={<Home/>} />
      <Route path='contact' element={<Contact />} />
      <Route path='login' element={<Login/>} />
      <Route path='signup' element={<Signup/>} />
      <Route path='*' element={<Error/>} />
    </Route>
    
    </>
  )
)


ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <RouterProvider router={router}/>
    
  </React.StrictMode>,
  
)
