import React from "react";
import axios from "axios";
import { useState } from "react";
import { useTime, useXY, useRotation } from "./Hooks.js";
import "./App.css";

export function Vehicle({
  width,
  height,
  initSpeed,
  initAcceleration,
  initLane,
  id,
  src,
}) {
  const [parameters, setParameters] = useState({
    speed: initSpeed,
    acceleration: initAcceleration,
    lane: initLane,
  });

  const time = useTime(id);
  const [x, y] = useXY(id, time, 980, 200);
  const rotation = useRotation(0, time);

  function handleSpeedChange(e) {
    e.preventDefault();
    const newSpeed = Math.min(Math.max(e.target.elements.speed.value, 0), 100);
    const newId = e.target.elements.speed.id;
    axios
      .put("http://localhost:8000/update-speed/", {
        id: newId,
        speed: newSpeed,
      })
      .then((response) => {
        console.log(
          "Speed updated successfully with ID:",
          newId,
          response.data
        );
      })
      .catch((error) => {
        console.error("Error updating speed with ID:", newId, error);
      });
  }

  function handleAccelerationChange(e) {
    e.preventDefault();
    const newAcceleration = Math.min(
      Math.max(e.target.elements.acceleration.value, 0),
      100
    );
    const newId = e.target.elements.acceleration.id;
    axios
      .put("http://localhost:8000/update-acceleration/", {
        id: newId,
        acceleration: newAcceleration,
      })
      .then((response) => {
        console.log(
          "Acceleration updated successfully with ID:",
          newId,
          response.data
        );
      })
      .catch((error) => {
        console.error("Error updating acceleration with ID:", newId, error);
      });
  }

  function handleLaneChange(e) {
    e.preventDefault();
    const newLane = Math.min(Math.max(e.target.elements.lane.value, 1), 4);
    const newId = e.target.elements.lane.id;
    axios
      .put("http://localhost:8000/update-lane/", {
        id: newId,
        lane: newLane,
      })
      .then((response) => {
        console.log("Lane updated successfully with ID:", newId, response.data);
      })
      .catch((error) => {
        console.error("Error updating lane with ID:", newId, error);
      });
  }

  return (
    <>
      <br />
      <br />
      <form onSubmit={handleSpeedChange}>
        <label>
          Speed:
          <input
            type="number"
            name="speed"
            id={id}
            value={parameters.speed}
            onChange={(e) => {
              setParameters({ ...parameters, speed: e.target.value });
            }}
            min={0}
            max={10}
          />
        </label>
        <button type="submit">Submit</button>
      </form>
      <br />
      <br />
      <form onSubmit={handleAccelerationChange}>
        <label>
          Acceleration:
          <input
            type="number"
            name="acceleration"
            id={id}
            value={parameters.acceleration}
            onChange={(e) => {
              setParameters({ ...parameters, acceleration: e.target.value });
            }}
            min={0}
            max={5}
          />
        </label>
        <button type="submit">Submit</button>
      </form>
      <br />
      <br />
      <form onSubmit={handleLaneChange}>
        <label>
          Lane:
          <input
            type="number"
            name="lane"
            id={id}
            value={parameters.lane}
            onChange={(e) => {
              setParameters({ ...parameters, lane: e.target.value });
            }}
            min={1}
            max={4}
          />
        </label>
        <button type="submit">Submit</button>
      </form>
      <img
        className="vehicle"
        src={src}
        alt={"vehicle"}
        style={{
          position: "absolute",
          left: x + "px",
          top: y + "px",
          width: width + "px",
          height: height + "px",
          transform: "rotate(" + rotation + "deg)",
          transformOrigin: "center center",
        }}
      />
    </>
  );
}
