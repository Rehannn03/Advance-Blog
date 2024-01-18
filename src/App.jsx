import { BrowserRouter } from "react-router-dom"
import {Navbar} from "./components/Navbar"
import Hero from "./components/Hero"

function App() {
  return (
    <BrowserRouter>
      <div className="bg bg-heroBG bg-cover h-[700px]">
        <Navbar />
        <Hero />
      </div>
    </BrowserRouter>
  )
}

export default App
