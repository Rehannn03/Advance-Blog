import { BrowserRouter,Route } from "react-router-dom"
import {Navbar} from "./components/Navbar"
import Hero from "./components/Hero"
import { Login } from "./components/Login"

function App() {
  return (
    <BrowserRouter>
      
      <div className="bg bg-heroBG bg-cover h-screen w-screen">
        <Navbar />
        <Hero />
      </div>
        

      
    </BrowserRouter>
  )
}

export default App
