import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import livefeed from './livefeed/livefeed'
import './Analytics.css'
import LineChart from './front.jsx'
import Button from '@mui/material/Button';
import hoowik from './assets/hoowik.png';


function Analytics() {

  const [start, setStart] = useState(false);

  const handleButtonClick = () => {
    setStart(!start);
    console.log("clicked")
    console.log(start)
  }

  return (
    <div className="back" style={{display: 'flex', flexDirection: 'column', justifyContent: 'center'}}>
        <div>
            <img style={{width: "150px", height: "auto", borderRadius: "50%", border:"4px solid #F3C556", borderColor:"#F3C556"}} src={hoowik} alt="Description of the image" />
        </div>
        <div style={{display: 'flex', justifyContent: 'center', alignItems: 'center'}}>
            <LineChart start={start}/>
        </div>
      <Button variant="contained" onClick={handleButtonClick} className="Button PurpleButton">
        Hoowik Start
      </Button>
    </div>
  )
}

export default Analytics