import starSVG from "../../assets/icons/star.svg"
import RoomCardSpecs from "../hotels/RoomCardSpecs"
import clockSVG from "../../assets/icons/clock.svg"
import locationSVG from "../../assets/icons/location.svg"
import dangerSVG from "../../assets/icons/danger.svg"
import doubleSVG from "../../assets/icons/double.svg"
import { useEffect, useState } from "react"

interface themePark {
    themeParkId: number
    name: string
    description: string
    price: number
    rating: number
    reviews: number
    capacity: number
    duration: string
    location: string
    ageLimit: string
    image: string
}

interface ThemeCardProps {
    role?: string
    edit?: boolean
    onClick?: () => void
    themePark?: themePark
}

export default function ThemeCard({ role, edit, onClick, themePark }: ThemeCardProps) {
    const allowAccess = role === "Admin" || role === "Ticketing-Staff"
    let buttonText = allowAccess ? "Select" : "Book Now"
    buttonText = edit ? "Edit Activity" : buttonText
    const imagePath = themePark?.image?.startsWith('/') ? themePark?.image : `/${themePark?.image}`
    const imgSrc = themePark?.image ? `http://localhost:8000${imagePath}` : ''
    const [bookingCount, setBookingCount] = useState(0)
    let bookingPercentage = (bookingCount || 0) / (themePark?.capacity || 1) * 100
    useEffect(() => {
        async function fetchThemeParkPage() {
            try {
                const response = await fetch('http://localhost:8000/api/theme-park/bookings', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ themeParkId: themePark?.themeParkId })
                });
                if (response.ok) {
                    const data = await response.json()
                    setBookingCount(data.bookingCount)
                }
            } catch (error) {
                console.error('Error loading page:', error)
            }
        }
        fetchThemeParkPage()
    }, [])
    return (
        <div className="w-[calc(50%-10px)] bg-white rounded-2xl overflow-hidden group">
            <div className=" relative w-full h-48 overflow-hidden bg-linear-to-r from-[#0E7490] to-[#06B6D3]">
                <img src={imgSrc} alt="Theme Park" className="w-full h-full object-cover hover:cursor-pointer group-hover:scale-110 transition-transform duration-300 ease-in-out" />
            </div>
            <div className="p-4">
                <div className="flex items-center justify-between mb-2">
                    <h3 className="text-lg font-medium text-[#333]">{themePark?.name}</h3>
                    <div className="flex items-center text-[#558282] text-sm">
                        <img src={starSVG} alt="Room" className="w-6 h-6 inline-block mr-1"/>
                        <p className="font-medium leading-[14px]"><span className="font-bold text-black">{themePark?.rating || '0.0'}</span> ({themePark?.reviews || 0} reviews)</p>
                    </div>
                </div>
                <p className="text-[#558282]">{themePark?.description}</p>
                <div className="flex flex-wrap items-center justify-between gap-3 mt-2">
                    <p className="bg-[#FEF2F2]/50 border border-red text-[#BB1C1C] rounded-full px-3 font-bold">Extreme</p>
                    <RoomCardSpecs icon={clockSVG} text={themePark?.duration || 'Not specified'} />
                    <RoomCardSpecs icon={locationSVG} text={themePark?.location || 'Not specified'} />
                    <RoomCardSpecs icon={dangerSVG} text={themePark?.ageLimit || 'Age 0+'} />
                </div>
                <div className="w-full mt-2">
                    <div className="flex items-center justify-between">
                        <div className="flex gap-2 text-[#558282]">
                            <img src={doubleSVG} className="w-5 h-5" />
                            <p className="text-sm">Today's Capacity</p>
                        </div>
                        <p className="text-[#0E7490] font-bold text-sm">{bookingCount || '0'}/{themePark?.capacity || '0'} booked ({bookingPercentage.toFixed(0)}%)</p>
                    </div>
                    <div className="w-full h-2 bg-[#E2F4F4] rounded-full mt-1 overflow-hidden">
                        <div className=" h-full bg-[#0E7490] rounded-full" style={{ width: `${bookingPercentage}%` }} />
                    </div>
                </div>
                <hr className="border-[#E8F5F5] border-y my-2" />
                <div className="flex items-center justify-between mt-3">
                    <div className="flex items-end text-[#0E7490]">
                        <h3 className="text-2xl font-bold">${themePark?.price || 'Not specified'}</h3>
                        <p className="text-sm">/person</p>
                    </div>
                    <button onClick={onClick} className="bg-[#0E7490] text-white px-4 py-2 rounded-full font-bold hover:bg-[#0891B2] transition-transform duration-200 ease-in-out hover:scale-105 hover:cursor-pointer">{buttonText}</button>
                </div>
            </div>
        </div>
    )
}