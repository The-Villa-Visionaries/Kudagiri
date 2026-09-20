import Header from "../components/common/Header"
import EventBanner from "../components/promotions/EventsBanner"
import PageTitle from "../components/common/PageTitle"
import FilterBar from "../components/common/FilterBar"
import PageIndex from "../components/common/PageIndex"
import FerryGrid from "../components/ferry/FerryGrid"
import Cart from "../components/ferry/Cart"
import { useEffect, useState } from "react"
import { useNavigate, useSearchParams } from "react-router-dom"
import Validation from "../components/ferry/Validation"

export default function Main() {
    const navigation = useNavigate();
    const [searchParams] = useSearchParams()

    const role = searchParams.get("role") || "Visitor"
    const allowAccess = role === "Admin" || role === "Ferry-Operator"
    useEffect(() => {
        if (!allowAccess) {
            navigation("/ferry")
        }
    }, [allowAccess, navigation])

    const title = "Ferry Routes"
    const description = "Book your island transit — smooth ferry trips, seaplanes, and direct routes await"
    const sideBar = allowAccess ? <Validation /> : <Cart />
    const [ferry, setFerry] = useState([])
    const [events, setEvents] = useState([])
    const userId = 1

    useEffect(() => {
        async function fetchFerryPage() {
            try {
                const response = await fetch('http://localhost:8000/api/ferry', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ requestId: userId })
                });
                if (response.ok) {
                    const data = await response.json()
                    setFerry(data.ferry)
                    setEvents(data.events)
                }
            } catch (error) {
                console.error('Error loading page:', error)
            }
        }
        fetchFerryPage()
    }, [])
    return (
        <div className="relative w-full h-full bg-[#F0FAFA] bg-[radial-gradient(#4bc0ad_1px,transparent_1px)] [background-size:16px_16px] px-9 py-4 flex flex-col gap-4 mt-16">
            <Header />
            <EventBanner events={events} />
            <PageTitle title={title} description={description} />
            <FilterBar Page="Ferry" />
            <div className="w-full flex items-start justify-between">
                <div className="min-w-4/6">
                    <FerryGrid role={role} ferry={ferry} />
                    <PageIndex />
                </div>
                {sideBar}
            </div>
        </div>
    )
}