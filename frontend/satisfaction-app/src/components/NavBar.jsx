import {Link} from "react-router-dom"
import '../App.css'

export default function NavBar(){
    return(
        <nav>
            <Link to="/">Home</Link>
            <Link to="/SatisfactionForm">Satisfaction Form</Link>
            <Link to="/Dashboard">Dashboard</Link>
        </nav>
    )
}