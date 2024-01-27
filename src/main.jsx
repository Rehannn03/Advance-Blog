import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import { RouterProvider, createBrowserRouter, createRoutesFromElements,Route } from 'react-router-dom'
import { Login } from './Pages/Login/Login.jsx'
import Home from './Pages/Home/Home.jsx'
import Error from './components/Error/Error.jsx'
import Signup from './Pages/Signup/Signup.jsx'
import AddBlog from './Pages/Add Blog/addBlog.jsx'
import About from './Pages/About/About.jsx'
const router = createBrowserRouter(
  createRoutesFromElements(
    <>
    
    <Route path='/' element={<App/>} >
      <Route path='' element={<Home/>} />
      <Route path='about' element={<About/>} />
      <Route path='login' element={<Login/>} />
      <Route path='signup' element={<Signup/>} />
      <Route path='*' element={<Error/>} />
    </Route>
    <Route path='/user'>
      <Route path='add_blog' element={<AddBlog/>}/>
    </Route>
    </>
  )
)


ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <RouterProvider router={router}/>
    
  </React.StrictMode>,
  
)
