import { useState, useEffect } from "react";
import axios from "axios";

const chatSocket = new WebSocket("ws://" + window.location.host + "/ws/chat/");

let board = new Array(10);
const initialArray = Array.from({ length: 10 }, () =>
  Array.from({ length: 10 }, () => 0)
);

export function useBoard(row, col, val) {
  const [array, setArray] = useState(initialArray);

  useEffect(() => {
    setArray((prevArray) => {
      const newArray = [...prevArray];
      newArray[row] = [...newArray[row]];
      newArray[row][col] = val;
      return newArray;
    });
  }, [row, col, val]);

  return array[row][col];
}

export function useTime(id) {
  const [time, setTime] = useState(0);
  const [speed, setSpeed] = useState(1);
  const [accel, setAccel] = useState(0);
  const [prevAccel, setPrevAccel] = useState(0);
  const [count, setCount] = useState(100);

  useEffect(() => {
    axios
      .get("http://localhost:8000/")
      .then(function (response) {
        const data = response.data;
        if (data) {
          const targetData = data.find((item) => item.id === id);
          if (targetData) {
            if (count < 100) {
              setSpeed(targetData.speed + accel * 0.05);
              axios
                  .put("http://localhost:8000/", {
                    id: id,
                    speed: targetData.speed + accel * 0.05,
                  })
                  .then((response) => {})
                  .catch((error) => {});
            } else {
              setSpeed(targetData.speed);
              setPrevAccel(accel);
              setAccel(targetData.acceleration);
              if (prevAccel !== accel) setCount(1);
            }
          } else {
            axios
              .put("http://localhost:8000/", {
                id: id,
                x: 0,
                y: 0,
                speed: 1,
              })
              .then((response) => {})
              .catch((error) => {});
          }
        }
      })
      .catch(function (error) {
        console.log(error);
      });
  });

  useEffect(() => {
    const intervalID = setInterval(() => {
        setTime((prevTime) => prevTime + 1 * speed);
        setCount((prevCount) => prevCount + 1);
    }, 20);
    return () => clearInterval(intervalID);
  });

  return time;
}

export function useXY(id, time, initX, initY) {
  const [x, setX] = useState(initX);
  const [y, setY] = useState(initY);
  const [lane, setLane] = useState(2);
  const laneRadius = { 1: 145, 2: 200, 3: 285, 4: 360 };

  useEffect(() => {
    axios
      .get("http://localhost:8000/")
      .then(function (response) {
        const data = response.data;
        if (data) {
          const targetData = data.find((item) => item.id === id);
          if (targetData) {
            setLane(targetData.lane);
            const targetData2 = data.find((item) => item.id !== id && item.lane === lane && (Math.sqrt(Math.pow(item.x - x, 2) + Math.pow(item.y - y, 2)) < 25));
            if (targetData2 && ((x < 980 && y < targetData2.y) || (x >= 980 && y > targetData2.y))) {
              if (lane === 1 && lane < 3) {
                setLane(targetData.lane + 1);
                axios
                  .put("http://localhost:8000/", {
                    id: id,
                    lane: lane + 1,
                  })
                  .then((response) => {})
                  .catch((error) => {});
              } else {
                setLane(targetData.lane - 1);
                axios
                  .put("http://localhost:8000/", {
                    id: id,
                    lane: lane - 1,
                  })
                  .then((response) => {})
                  .catch((error) => {});
              } 
            }
          }
        }
      })
      .catch(function (error) {
        console.log(error);
      });
    });

    let radius = laneRadius[lane];

    useEffect(() => {
      const intervalID = setInterval(() => {
        setX(initX + radius * Math.sin((time * Math.PI) / 180));
        setY(initY + radius * Math.cos((time * Math.PI) / 180));
        axios
          .put("http://localhost:8000/", {
            id: id,
            x: initX + radius * Math.sin((time * Math.PI) / 180),
            y: initY + radius * Math.cos((time * Math.PI) / 180),
          })
          .then((response) => {})
          .catch((error) => {});
      }, 20);
      return () => clearInterval(intervalID);
    });

  return [x, y];
}

export function useRotation(initRotation, time) {
  const [rotation, setRotation] = useState(initRotation);

  useEffect(() => {
    const intervalID = setInterval(() => {
      setRotation(initRotation - time);
    }, 20);
    return () => clearInterval(intervalID);
  });
  return rotation;
}
