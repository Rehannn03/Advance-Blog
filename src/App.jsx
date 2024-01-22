import { Login } from "./Pages/Login/Login.jsx"
import Home from "./Pages/Home/Home.jsx"
import { Outlet } from "react-router-dom"
import {Navbar} from "./components/Navbar/Navbar.jsx"


function App() {
  return (
    
      <>
        <div>
          <Navbar/>
          <Outlet/>
        </div>
      </>
      // <div className="bg bg-heroBG bg-cover h-screen w-screen">
      //   <Home/>
        
      // </div>
        

      
    
  )
}

export default App
