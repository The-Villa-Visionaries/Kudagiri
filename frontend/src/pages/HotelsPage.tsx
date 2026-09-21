import PromoBanner, { type Promotion } from "../components/promotions/PromoBanner"
import RoomGrid from "../components/hotels/RoomGrid"
import PageTitle from "../components/common/PageTitle"
import FilterBar from "../components/common/FilterBar"
import PageIndex from "../components/common/PageIndex"
import BookingSummary from "../components/hotels/BookingSummary"
import Header from "../components/common/Header"
import { useEffect, useState } from "react"

export default function Main() {
    const title = "Hotels & Rooms"
    const description = "luxury stays and beachfront suites — your gateway to an unforgettable island stay"
    const [hotels, setHotels] = useState([])
    const [promotions, setPromotions] = useState<Promotion[]>([])
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
                    setPromotions(data.promotions)
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
            <PromoBanner promo={promotions[0]} />
            <PageTitle title={title} description={description} />
            <FilterBar Page="Hotels" />
            <div className="w-full flex items-start justify-between">
                <div className="min-w-4/6">
                    <RoomGrid hotels={hotels} />
                    <PageIndex />
                </div>
                <BookingSummary />
            </div>
        </div>
    )
}