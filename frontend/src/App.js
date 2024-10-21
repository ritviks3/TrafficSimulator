// import * as ReactDOM from 'react-dom';
import React from "react";
import axios from "axios";
import { useState, useEffect } from "react";
import { Vehicle } from "./Vehicle.js";
import "./App.css";
import car from "./Images/car.png";
import truck from "./Images/truck.png";
import { DndProvider } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";
import TrafficLight from "./TrafficLight.js";

let carId = 0;
let truckId = 6;
let board = new Array(10);
for (let i = 0; i < board.length; i += 1) board[i] = new Array(10).fill(0);

function importAll(r) {
  let images = {};
  r.keys().forEach((item, index) => {
    images[item.replace("./", "")] = r(item);
  });
  return images;
}

function Piece(p) {
  const [value, setValue] = useState(board[p.y][p.x]);
  const cls = ["piece"];
  if (value !== 0) {
    if (value % 7 === 0) cls.push("piece");
    else if (value % 7 === 1) cls.push("roadEW");
    else if (value % 7 === 2) cls.push("roadNS")
    else if (value % 7 === 3) cls.push("roadNE");
    else if (value % 7 === 4) cls.push("roadNW");
    else if (value % 7 === 5) cls.push("roadSE");
    else if (value % 7 === 6) cls.push("roadSW");
  }
  return (
    <div
      className={cls.join(" ")}
      onClick={() => {
        board[p.y][p.x] += 1;
        setValue(board[p.y][p.x]);
      }}
    >
    </div>
  );
}

function Board() {
  return (
    <div className="board">
      {board.map((b, iy) => (
        <div key={iy}>
          {b.map((a, ix) => (
            <Piece key={ix} x={ix} y={iy} />
          ))}
        </div>
      ))}
    </div>
  );
}

export default function App() {
  const [cars, setCars] = useState([]);
  const [trucks, setTrucks] = useState([]);
  const [carLimit, setCarLimit] = useState(false);
  const [truckLimit, setTruckLimit] = useState(false);
  const [trafficLights, setTrafficLights] = useState([]);
  const [idCounter, setIdCounter] = useState(0);
  const [vehicles, setVehicles] = useState([]);
  const images = importAll(
    require.context("./Images/tracks", false, /\.(png|jpe?g|svg)$/)
  );

  useEffect(() => {
    axios
      .delete("http://localhost:8000/")
      .then((response) => {
        console.log(response.data);
      })
      .catch((error) => {
        console.error("There was an error with the DELETE request: ", error);
      });
  }, []);

  const handleSpawnCar = () => {
    if (cars.length < 5) {
      setCars([
        ...cars,
        {
          id: carId++,
          car: (
            <Vehicle
              width={50}
              height={25}
              initSpeed={1}
              initAcceleration={0}
              initLane={2}
              id={carId}
              src={car}
              color={"black"}
            />
          ),
        },
      ]);
    } else {
      setCarLimit(true);
    }
  };

  const handleSpawnTruck = () => {
    if (trucks.length < 5) {
      setTrucks([
        ...trucks,
        {
          id: truckId++,
          truck: (
            <Vehicle
              width={70}
              height={50}
              initSpeed={0.5}
              initAcceleration={0}
              initLane={2}
              id={truckId}
              src={truck}
              color={"black"}
            />
          ),
        },
      ]);
    } else {
      setTruckLimit(true);
    }
  };

  const addTrafficLight = () => {
    const newTrafficLight = {
      id: idCounter,
      x: 200,
      y: 300,
      state: "red",
    };

    setTrafficLights([...trafficLights, newTrafficLight]);
    setIdCounter(idCounter + 1);
  };

  const toggleTrafficLight = (id, color) => {
    const updatedTrafficLights = trafficLights.map((light) => {
      if (light.id === id) {
        return { ...light, state: color };
      }
      return light;
    });

    setTrafficLights(updatedTrafficLights);
  };

  const onMoveTrafficLight = (id, newX, newY) => {
    const updatedTrafficLights = trafficLights.map((light) => {
      if (light.id === id) {
        return { ...light, x: newX, y: newY };
      }
      return light;
    });
    setTrafficLights(updatedTrafficLights);
  };

  const calculateCarColor = (currentCar) => {
    console.log(currentCar.car.props.initSpeed);
    const minDistance = Math.min(
      ...cars
        .filter((tempCar) => tempCar.id !== currentCar.id)
        .map((tempCar) =>
          Math.sqrt(
            Math.pow(
              tempCar.car.props.initSpeed - currentCar.car.props.initSpeed,
              2
            ) +
              Math.pow(
                tempCar.car.props.initAcceleration -
                  currentCar.car.props.initAcceleration,
                2
              )
          )
        )
    );
    console.log(currentCar.id, minDistance);
    return minDistance < 10 ? "red" : "green";
  };

  return (
    <DndProvider backend={HTML5Backend}>
      <div className="parent">
        <div className="child-stats">
          <br />
          <span>
          <button type="submit" onClick={(e) => handleSpawnCar(e)}>Spawn car</button>
          <ul style={{ listStyleType: "none", padding: 0 }}>
            {cars.length <= 5 &&
              cars.map((car) => <li key={car.id}>{car.car}</li>)}
          </ul>
          </span>
          {carLimit && <r> Maximum car limit reached.</r>}
          <button type="submit" onClick={(e) => handleSpawnTruck(e)}>Spawn truck</button>
          <ul style={{ listStyleType: "none", padding: 0 }}>
            {trucks.length <= 5 &&
              trucks.map((truck) => <li key={truck.id}>{truck.truck}</li>)}
          </ul>
          {truckLimit && <r> Maximum truck limit reached.</r>}
          <button type="submit" onClick={addTrafficLight}>Add Traffic Light</button>
          <div className="simulation-container">
            {trafficLights.map((light) => (
              <TrafficLight
                key={light.id}
                id={light.id}
                x={light.x}
                y={light.y}
                state={light.state}
                onToggle={toggleTrafficLight}
                onMove={onMoveTrafficLight}
              />
            ))}
          </div>
        </div>
        <div className="child-board">
          <Board />
        </div>
      </div>
    </DndProvider>
  );
}