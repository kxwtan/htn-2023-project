import React from "react";
import { useState, useCallback, useEffect } from "react"
import { Line } from "react-chartjs-2";
import Chart from "chart.js/auto";
import "./front.css"





const options = {
  scales: {
    x: {
      ticks: {
        color: "#00FFF6",
      },
      grid: {
        color: "#F3C556", // White grid lines for x-axis
      },
    },
    y: {
      ticks: {
        color: "#00FFF6",
      },
      grid: {
        color: "#F3C556", // White grid lines for y-axis
      },
    },
  },
  plugins: {
    legend: {
      display: true,
      position: "top",
    },
  },
};


const LineChart = (props) => {

  let zvec = []
  let timestamp = []
  const [origin, setOrigin] = useState(null);
  const [chartData, setChartData] = useState({
    labels: [],
    datasets: [
      {
        label: "Distance v Time (Milliseconds)",
        backgroundColor: "#00FFF6", // Dark green background
        borderColor: "#00FFF6", // Dark green border color
        borderWidth: 2,
        data: [],
      },
    ],
  })
  console.log("props.start")
  console.log(props.start)
  const getData = async () => {
    try {
        const res = await fetch("http://127.0.0.1:5000/get_latest_et_data");
        const blocks = await res.json();
    
        setOrigin(blocks);
    } catch (e) {
        console.log(e);
    }
  };

  useEffect(() => {
    const intervalCall = setInterval(() => {
        getData();
    }, 1000);

    if (origin != null && origin != []) {
      for (let index = 0; index < origin['data'].length; index++ ) {
        zvec.push(origin['data'][index][2])
        timestamp.push(origin['data'][index][4])
      }
    }

    
    setChartData((prev)=>({...prev, labels: timestamp, datasets : [{...prev.datasets[0], data:zvec}] }))
    return () => {
      // clean up
      clearInterval(intervalCall);
    };
  },[origin]);






  return (
    <div style={{width:"70vw", height:"65vh"}}>
      <Line  data={chartData} options={options} />
    </div>
  );
};

export default LineChart;