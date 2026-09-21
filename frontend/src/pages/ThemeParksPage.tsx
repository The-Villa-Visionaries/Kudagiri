import { useSearchParams } from "react-router-dom"
import Header from "../components/common/Header"
import PageIndex from "../components/common/PageIndex"
import PageTitle from "../components/common/PageTitle"
import FilterBar from "../components/common/FilterBar"
import EventsBanner from "../components/promotions/EventsBanner"
import ThemeGrid from "../components/theme-park/ThemeGrid"
import Cart from "../components/theme-park/Cart"
import Validation from "../components/theme-park/Validation"
import { useEffect, useState } from "react"

export default function Main() {
    const [searchParams] = useSearchParams()

    const role = searchParams.get("role") || "Visitor"
    const allowAccess = role === "Admin" || role === "Ticketing-Staff"

    const title = allowAccess ? "Theme Park Activities Management" : "Theme Park Activities"
    const description = allowAccess ? "Configure attraction capacity, edit activity details, and monitor live guest volume" : "Experience world-class thrills — book rides, shows, and beach activities"
    const sideBar = allowAccess ? <Validation /> : <Cart />
    const [themePark, setThemePark] = useState([])
    const [events, setEvents] = useState([])
    const userId = 1

    useEffect(() => {
        async function fetchThemeParkPage() {
            try {
                const response = await fetch('http://localhost:8000/api/theme-park', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ requestId: userId })
                });
                if (response.ok) {
                    const data = await response.json()
                    setThemePark(data.themePark)
                    setEvents(data.events)
                }
            } catch (error) {
                console.error('Error loading page:', error)
            }
        }
        fetchThemeParkPage()
    }, [])
    return (
        <div className="relative w-full h-full bg-[#F0FAFA] bg-[radial-gradient(#4bc0ad_1px,transparent_1px)] [background-size:16px_16px] px-9 py-4 flex flex-col gap-4 mt-16">
            <Header />
            {!allowAccess && (<EventsBanner events={events} />)}
            <PageTitle title={title} description={description} />
            <FilterBar Page="Theme Park" />
            <div className="w-full flex items-start justify-between">
                <div className="min-w-4/6">
                    <ThemeGrid role={role} themePark={themePark} />
                    <PageIndex />
                </div>
                {sideBar}
            </div>
        </div>
    )
}