import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import livefeed from './livefeed/livefeed'
import LineChart from './front.jsx'
import Button from '@mui/material/Button';
import hoowik from './assets/hoowik.png';
import { Route, createBrowserRouter, createRoutesFromElements, RouterProvider } from 'react-router-dom';
import Analytics from './Analytics'
import Home from './home'

const router = createBrowserRouter(
  createRoutesFromElements(
    <Route path="/">
      <Route index element={<Home/>}/>
      <Route path="analytics" element={<Analytics/>}/>
    </Route>
  )
)


function App({routes}) {

  return (
    <>
      <RouterProvider router={router}/>
    </>
  )
}

export default App