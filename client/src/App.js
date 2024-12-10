// 📚 Review With Students:
// Request response cycle
//Note: This was build using v5 of react-router-dom
import { Outlet, useNavigate } from 'react-router-dom'
import { createGlobalStyle } from 'styled-components'
import { useEffect, useState } from 'react'
import Header from './components/navigation/Header'
import toast, { Toaster } from "react-hot-toast"
import "./App.css"

const getCookie = (name) => {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

function App() {
  const [currentUser, setCurrentUser] = useState(null)
  const [productions, setProductions] = useState([])
  const [production_edit, setProductionEdit] = useState(false)
  const navigate = useNavigate()

  //5.✅ GET Productions
  useEffect(() => {
    (async () => {
      const resp = await fetch("/api/v1/productions", {
        headers: {
          "X-CSRF-TOKEN": getCookie("csrf_access_token")
        }
      })
      const data = await resp.json()
      if (resp.ok) {
        setProductions(data)
      } else {
        toast.error(data.error)
      }
    })()
  }, [])
  const updateUser = (value) => setCurrentUser(value)

  useEffect(() => {
    (async () => {
      const resp = await fetch("/api/v1/current-user", {
        headers: {
          "X-CSRF-TOKEN": getCookie("csrf_access_token")
        }
      })
      const data = await resp.json()
      if (resp.ok) {
        updateUser(data)
      } else {
        const resp = await fetch("/api/v1/refresh", {
          method: "POST",
          headers: {
            "X-CSRF-TOKEN": getCookie("csrf_refresh_token")
          }
        })
        const refreshData = await resp.json()
        if (resp.ok) {
          updateUser(refreshData)
        } else {
          toast.error(data.error)
          navigate("/registration")
        }
      }
    })()
  }, [navigate])

  const addProduction = (production) => {
    setProductions(productions => [...productions, production])
  }
  const updateProduction = (updated_production) => setProductions(productions => (
    productions.map(production => production.id === updated_production.id ? updated_production : production)
  ))
  const deleteProduction = (deleted_production_id) => setProductions(productions => (
    productions.filter((production) => production.id !== parseInt(deleted_production_id))
  ))

  const handleEdit = (production) => {
    setProductionEdit(production)
    navigate(`/productions/${production.id}/edit`)
  }


  return (
    <>
      <GlobalStyle />
      <Header handleEdit={handleEdit} currentUser={currentUser} updateUser={updateUser} />
      <Toaster />
      <Outlet context={{ addProduction, updateProduction, deleteProduction, productions, production_edit, handleEdit, updateUser, currentUser }} />
    </>
  )
}

export default App

const GlobalStyle = createGlobalStyle`
    body{
      background-color: black; 
      color:white;
    }
    `

