import { useState, useEffect } from 'react';
import '../App.css'

export default function SatisfactionForm() {
  const [age, setAge] = useState(null);
  const [travelClass, setTravelClass] = useState('');
  const [typeOfTravel, setTypeOfTravel] = useState('');
  const [customerType, setCustomerType] = useState('');
  const [flightDistance, setFlightDistance] = useState(null);
  const [onlineBoarding, setOnlineBoarding] = useState(null);
  const [seatComfort, setSeatComfort] = useState(null);
  const [inflightEntertainment, setInflightEntertainment] = useState(null);
  const [onBoardService, setOnBoardService] = useState(null);
  const [legRoomService, setLegRoomService] = useState(null);
  const [cleanliness, setCleanliness] = useState(null);
  const [predictedSatisfaction, setPredictedSatisfaction] = useState(null);

  async function handleSubmit(e) {
  e.preventDefault();
  const passengerData = {
            Age: age,
            Class: travelClass,
            Type_of_Travel: typeOfTravel,
            Customer_Type: customerType,
            Flight_Distance: flightDistance,
            Online_boarding: onlineBoarding,
            Seat_comfort: seatComfort,
            Inflight_entertainment: inflightEntertainment,
            On_board_service: onBoardService,
            Leg_room_service: legRoomService,
            Cleanliness: cleanliness
      }
  try {
    const response = await fetch("http://127.0.0.1:8000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(passengerData),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();
    const prediction = data.predicted_satisfaction;

    setPredictedSatisfaction(prediction); // Si tu veux l'afficher ailleurs aussi

    const addResponse = await fetch("http://127.0.0.1:8000/add_passenger", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(passengerData),
    });

    const addData = await addResponse.json();
    console.log("Passenger added to DB:", addData);

    const message = prediction === 1 ? "satisfied" : "not satisfied";
    alert(`Thank you for your submission, see you soon.\nCustomer is ${message} and Saved to DB successfully!`);
  }catch (error) {
    console.error("Error during API request:", error);
    alert("An error occurred while submitting the form. Please try again.");
  }
  }
  return (
    <div>
      <form onSubmit={handleSubmit}>
        <h2>Customer Satisfaction Feedback</h2>
        <p>
          We value your feedback! Please take a moment to rate your recent flight experience.
          <br />  
          Your input helps us improve our services and better meet your expectations.
        </p>     
        <br /><br />
        <div>
          <label htmlFor="age">Age: </label>
          <input 
            htmlFor="age" 
            type="number" 
            value={age}
            onChange={(e) => setAge(e.target.value)}
            min={0} 
            required /> 
        </div>
        <br />
        <div>
          <label htmlFor="travelClass">Class: </label>
          <select 
            id="travelClass" 
            name="travelClass" 
            value={travelClass}
            onChange={(e) => setTravelClass(e.target.value)} 
            required >
            <option value="">-- Choose a class --</option>
            <option value="Business">Business</option>
            <option value="Eco Plus">Eco Plus</option>
            <option value="Eco">Eco</option>
          </select>
        </div>
        <br />
        <div>
          <label htmlFor="typeOfTravel">Type of travel: </label>
          <select 
            id="typeOfTravel" 
            name="typeOfTravel" 
            value={typeOfTravel}
            onChange={(e) => setTypeOfTravel(e.target.value)} 
            required>
            <option value="">-- Choose a travel type --</option>
            <option value="Business travel">Business Travel</option>
            <option value="Personal Travel">Personal Travel</option>
          </select>
        </div>
        <br />
        <div>
          <label htmlFor="customerType">Customer type: </label>
          <select 
            id="customerType" 
            name="customerType" 
            value={customerType}
            onChange={(e) => setCustomerType(e.target.value)} 
            required>
            <option value="">-- Choose a class --</option>
            <option value="Loyal Customer">Loyal Customer</option>
            <option value="disloyal Customer">Disloyal Customer</option>
          </select>
        </div>
        <br />
        <div>
          <label htmlFor="flightDistance">Flight Distance: </label>
          <input  
            type="number" 
            id="flightDistance" 
            value={flightDistance}
            onChange={(e) => setFlightDistance(e.target.value)}
            min={0} 
            required />
        </div>
        <br />
        <div>
          <label>Online Boarding:</label>
          {[0, 1, 2, 3, 4, 5].map((value) => (
            <label key={`online-${value}`}>
              <input 
                type="radio" 
                name="onlineBoarding" 
                value={value} 
                checked={onlineBoarding == value}
                onChange={(e) => setOnlineBoarding(e.target.value)}
                required />
              {value}
            </label>
          ))}
        </div>
        <br />
        <div>
          <label>Seat Comfort:</label>
          {[0, 1, 2, 3, 4, 5].map((value) => (
            <label key={`seat-${value}`}>
              <input 
                type="radio" 
                name="seatComfort" 
                value={value} 
                checked={seatComfort == value}
                onChange={(e) => setSeatComfort(e.target.value)}
                required />
              {value}
            </label>
          ))}
        </div>
        <br />
        <div>
          <label>Inflight Entertainment:</label>
          {[0, 1, 2, 3, 4, 5].map((value) => (
            <label key={`entertainment-${value}`}>
              <input 
                type="radio" 
                name="inflightEntertainment"
                value={value}
                checked={inflightEntertainment == value}
                onChange={(e) => setInflightEntertainment(e.target.value)}
                required />
              {value}
            </label>
          ))}
        </div>
        <br />
        <div>
          <label>On-board Service:</label>
          {[0, 1, 2, 3, 4, 5].map((value) => (
            <label key={`service-${value}`}>
              <input 
                type="radio"
                name="onBoardService"
                value={value}
                checked={onBoardService == value}
                onChange={(e) => setOnBoardService(e.target.value)}
                required />
              {value}
            </label>
          ))}
        </div>
        <br />
        <div>
          <label>Leg Room Service:</label>
          {[0, 1, 2, 3, 4, 5].map((value) => (
            <label key={`legroom-${value}`}>
              <input 
                type="radio" 
                name="legRoomService"
                value={value}
                checked={legRoomService == value}
                onChange={(e) => setLegRoomService(e.target.value)}
                required />
              {value}
            </label>
          ))}
        </div>
        <br />
        <div>
          <label>Cleanliness:</label>
          {[0, 1, 2, 3, 4, 5].map((value) => (
            <label key={`cleanliness-${value}`}>
              <input 
                type="radio" 
                name="cleanliness"
                value={value}
                checked={cleanliness == value}
                onChange={(e) => setCleanliness(e.target.value)}
                required />
              {value}
            </label>
          ))}
        </div>
        <br />
        <button type="submit">Submit</button>
      </form>
    </div>
  )
}