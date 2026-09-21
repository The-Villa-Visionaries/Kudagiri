import { useNavigate, useSearchParams } from "react-router-dom"
import Header from "../components/common/Header"
import PageIndex from "../components/common/PageIndex"
import PageTitle from "../components/common/PageTitle"
import FilterBar from "../components/common/FilterBar"
import { useEffect, useState } from "react"
import RoomGrid from "../components/hotels/RoomGrid"
import Edit from "../components/hotels/Edit"
import Create from "../components/hotels/Create"

export default function Main() {
    const navigation = useNavigate();
    const [searchParams] = useSearchParams()
    const [switchState, setSwitchState] = useState(true)

    const role = searchParams.get("role") || "Visitor"
    const allowAccess = role === "Admin" || role === "Hotel-Staff"
    useEffect(() => {
        if (!allowAccess) {
            navigation("/Hotels")
        }
    }, [allowAccess, navigation])

    const title = "Manage Hotels"
    const description = "Control room inventories, manage guest reservations, and configure promotional offers"
    const [hotels, setHotels] = useState([])
    const userId = 1

    useEffect(() => {
        async function fetchHotelPage() {
            try {
                const response = await fetch('http://localhost:8000/api/hotel', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ requestId: userId })
                });
                if (response.ok) {
                    const data = await response.json()
                    setHotels(data.hotels)
                }
            } catch (error) {
                console.error('Error loading page:', error)
            }
        }
        fetchHotelPage()
    }, [])
    return (
        <div className="relative w-full h-full bg-[#F0FAFA] bg-[radial-gradient(#4bc0ad_1px,transparent_1px)] [background-size:16px_16px] px-9 py-4 flex flex-col gap-4 mt-16">
            <Header />
            <PageTitle title={title} description={description} />
            <FilterBar Page="Hotels" Create={true} onCreateClick={() => setSwitchState(true)} />
            <div className="w-full flex items-start justify-between">
                <div className="min-w-4/6">
                    <RoomGrid role={role} edit={true} onClick={() => setSwitchState(false)} hotels={hotels} />
                    <PageIndex />
                </div>
                {switchState ? <Create /> : <Edit />}
            </div>
        </div>
    )
}