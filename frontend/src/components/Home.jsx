import { Link } from "react-router-dom";
import '../App.css';

export default function Home() {
  return (
    <div className="home-container">
      <h1>Welcome!</h1>
      <p>
        Discover our passenger satisfaction tracking platform.
      </p>

      <ul>
        <li>Fill out the form to evaluate a passenger's experience.</li>
        <li>View satisfaction trends on the Dashboard.</li>
        <li>Identify services to improve to better satisfy your customers.</li>
        <li>Spot <strong>at-risk</strong> passenger profiles to act quickly.</li>
      </ul>
    </div>
  )
}
