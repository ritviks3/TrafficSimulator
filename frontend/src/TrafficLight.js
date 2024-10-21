import React from "react";
import { useDrag } from "react-dnd";
import trafficLightRed from "./Images/trafficLightred.png";
import trafficLightYellow from "./Images/trafficLightyellow.png";
import trafficLightGreen from "./Images/trafficLightgreen.png";
const trafficLights = {
  red: trafficLightRed,
  yellow: trafficLightYellow,
  green: trafficLightGreen,
};
const TrafficLight = ({ id, x, y, state, onToggle, onMove }) => {
  const getNextState = (currentState) => {
    switch (currentState) {
      case "red":
        return "yellow";
      case "yellow":
        return "green";
      case "green":
        return "red";
      default:
        return "red"; // Default to red if the state is unknown
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleDrop = (e) => {
    const { clientX, clientY } = e;
    onMove(id, clientX, clientY);
  };

  return (
    <div
      onDragOver={handleDragOver}
      onDrop={handleDrop}
      style={{
        width: "100vw",
        height: "100vh",
        position: "absolute",
        overflow: "hidden",
      }}
    >
      <img
        style={{
          position: "absolute",
          left: x,
          top: y,
          cursor: "move",
        }}
        onClick={() => onToggle(id, getNextState(state))}
        draggable
        src={trafficLights[state]}
        alt="Traffic Light"
      />
    </div>
  );
};

export default TrafficLight;
