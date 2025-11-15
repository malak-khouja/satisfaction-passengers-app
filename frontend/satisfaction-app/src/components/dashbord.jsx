import { useEffect, useState } from "react";
import Plot from "react-plotly.js";
import '../App.css';

export default function Dashboard() {
  const [passengers, setPassengers] = useState([]);
  const [metrics, setMetrics] = useState(null);
  const [selectedAgeRange, setSelectedAgeRange] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/passengers/")
      .then(res => res.json())
      .then(json => setPassengers(json))
      .catch(err => console.error(err));
  }, []);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/metrics/overview")
      .then(res => res.json())
      .then(json => setMetrics(json))
      .catch(err => console.error(err));
  }, []);

  const filteredData = passengers.filter(p => !selectedAgeRange || (p.Age >= selectedAgeRange[0] && p.Age <= selectedAgeRange[1]));

  const calculateSatisfactionByService = (service) => {
    const result = [];
    for (let note = 1; note <= 5; note++) {
      const group = filteredData.filter(p => p[service] === note);
      const satisfied = group.filter(p => p.predicted_satisfaction === 1).length;
      result.push(group.length === 0 ? 0 : satisfied / group.length);
    }
    return result;
  };

  const getServiceVariation = (service) => {
    const props = calculateSatisfactionByService(service);
    let maxDiff = 0;
    for (let i = 1; i < props.length; i++) {
      maxDiff = Math.max(maxDiff, Math.abs(props[i] - props[i - 1]));
    }
    return maxDiff;
  };

  const services = ["Online_boarding","Seat_comfort","Inflight_entertainment","On_board_service","Leg_room_service","Cleanliness"];
  const servicesSorted = services.map(s => ({ service: s, variation: getServiceVariation(s) })).sort((a,b) => b.variation - a.variation);
  const dissatisfiedPassengers = filteredData.filter(p => p.predicted_satisfaction === 0);
  const serviceRisk = services.map(s => ({ service: s, risk: dissatisfiedPassengers.filter(p => p[s] <= 2).length / (dissatisfiedPassengers.length || 1) }))
                              .sort((a,b) => b.risk - a.risk);

  return (
    <div className="dashboard-container">
      <h2>Passenger Satisfaction Dashboard</h2>

      {metrics && (
        <div className="metrics-row">
          <div className="metric-card metric-blue">
            <h4>Total Passengers</h4>
            <p>{metrics.total}</p>
          </div>
          <div className="metric-card metric-green">
            <h4>% Satisfied</h4>
            <p>{(metrics.satisfied_pct * 100).toFixed(1)}%</p>
          </div>
          <div className="metric-card metric-purple">
            <h4>Average Last 30 Days</h4>
            <p>{metrics.avg_last_month}</p>
          </div>
          <div className="metric-card metric-red">
            <h4>At-Risk Passengers</h4>
            <p>{metrics.at_risk}</p>
          </div>
        </div>
      )}

      <h3>Satisfaction by Age Range</h3>
      {passengers.length > 0 ? (
        <Plot
          className="plot-container"
          data={[{ x: passengers.map(p => p.Age), type: "histogram", xbins: {start:0,end:100,size:10} }]}
          layout={{ xaxis: { title: "Age" }, yaxis: { title: "Number of passengers" }, bargap: 0.4 }}
          onClick={(event) => {
            const binCenter = event.points[0].x;
            const binSize = event.points[0].data.xbins.size || 10;
            setSelectedAgeRange([binCenter - binSize/2, binCenter + binSize/2]);
          }}
        />
      ) : <p>Loading passengers...</p>}

      <h3>Proportion of Satisfied Passengers per Service</h3>
      <Plot
        className="plot-container"
        data={services.map(s => ({ y: calculateSatisfactionByService(s), x: [1,2,3,4,5], type: "bar", name: s.replace("_"," ") }))}
        layout={{ barmode: "group", xaxis: { title: "Service Rating" }, yaxis: { title: "Proportion Satisfied", range:[0,1] } }}
      />
      <br />
      <button onClick={() => setSelectedAgeRange(null)}>Reset Filter</button>

      <h3>Services Influence on Satisfaction</h3>
      <Plot
        className="plot-container"
        data={[{ x: servicesSorted.map(s=>s.variation), y: servicesSorted.map(s=>s.service), type:"bar", orientation:"h", marker:{color:"orange"} }]}
        layout={{ xaxis: { title:"Satisfaction Variation" }, yaxis: { title:"Service" } }}
      />

      <h3>At-Risk Passengers (Dissatisfied)</h3>
      <table>
        <thead>
          <tr>
            <th>ID</th><th>Age</th><th>Online Boarding</th><th>Seat Comfort</th><th>Inflight Entertainment</th><th>On-board Service</th><th>Leg Room Service</th><th>Cleanliness</th>
          </tr>
        </thead>
        <tbody>
          {dissatisfiedPassengers.map(p => (
            <tr key={p.ID}>
              <td>{p.ID}</td><td>{p.Age}</td><td>{p.Online_boarding}</td><td>{p.Seat_comfort}</td><td>{p.Inflight_entertainment}</td><td>{p.On_board_service}</td><td>{p.Leg_room_service}</td><td>{p.Cleanliness}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <h3>Main Causes of Dissatisfaction</h3>
      <Plot
        className="plot-container"
        data={[{ x: serviceRisk.map(s=>s.risk), y: serviceRisk.map(s=>s.service), type:"bar", orientation:"h", marker:{color:"red"} }]}
        layout={{ xaxis:{title:"Proportion of dissatisfied passengers"}, yaxis:{title:"Service"} }}
      />
    </div>
  )
}
