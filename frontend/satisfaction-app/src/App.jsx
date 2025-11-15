import { Routes, Route } from 'react-router-dom'
import NavBar from './components/Navbar'
import Home from './components/Home'
import SatisfactionForm from './components/SatisfactionForm'
import Dashboard from './components/dashbord.jsx';
import './App.css'


export default function App() {
  return (
    <div>
      <header>
        <NavBar />
        <br />
      </header>
      <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/SatisfactionForm" element={<SatisfactionForm />} />
          <Route path="/Dashboard" element={<Dashboard />} />
          <Route path="*" element={<h2>Page Not Found</h2>} />
        </Routes>
      <footer>
      </footer>
    </div>
  )
}



