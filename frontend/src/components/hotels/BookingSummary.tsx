import calenderSVG from "../../assets/icons/calendar.svg"
import doubleSVG from "../../assets/icons/double.svg"
import InputBox from "../common/InputBox"
import promoSVG from "../../assets/icons/promo-d.svg"
import { useState } from "react"

interface Hotel {
    hotelId: number
    name: string
    description: string
    price: number
    rating: number
    reviews: number
    capacity: number
    roomSize: string
    bedType: string
    amenities: string
    offers: string
    image: string
}


interface BookingSummaryProps {
    selectedHotel: Hotel | null
}

export default function BookingSummary({ selectedHotel }: BookingSummaryProps) {
    const [checkInDate, setCheckInDate] = useState<string>('')
    const [checkOutDate, setCheckOutDate] = useState<string>('')
    const [guestCount, setGuestCount] = useState<number>(1)
    const [promoCode, setPromoCode] = useState<string>('')
    const imagePath = selectedHotel?.image?.startsWith('/') ? selectedHotel?.image : `/${selectedHotel?.image}`
    const imgSrc = selectedHotel?.image ? `http://localhost:8000${imagePath}` : ''
    const calculateNights = () => {
        if (!checkInDate || !checkOutDate) return 0
        const [inYear, inMonth, inDay] = checkInDate.split('-').map(Number)
        const [outYear, outMonth, outDay] = checkOutDate.split('-').map(Number)
        const start = new Date(inYear, inMonth - 1, inDay)
        const end = new Date(outYear, outMonth - 1, outDay)
        const diffTime = end.getTime() - start.getTime()
        const diffDays = Math.round(diffTime / (1000 * 60 * 60 * 24))
        
        return diffDays > 0 ? diffDays : 0
    }
    const totalNights = calculateNights()
    return (
        <div className="sticky top-19 w-full rounded-2xl bg-white overflow-hidden mt-9">
            <div className="w-full h-25 bg-linear-to-r from-[#0E7490] to-[#06B6D3] flex flex-col justify-center gap-2 p-4 text-white">
                <h1 className="text-lg font-black">Your Booking Summary</h1>
                <p className="text-sm pl-2">Complete the details below to reserve</p>
            </div>
            <div className="w-full p-4 flex flex-col gap-4">
                <div className="w-full border-dashed border-[#E8F5F5] border-3 rounded-2xl flex flex-col items-center justify-center text-[#558282] overflow-hidden">
                    {selectedHotel ? (
                        <div className="relative w-full h-full flex items-center justify-center border border-white rounded-2xl">
                            <img src={imgSrc} alt="Hotel" className="w-full h-32 object-cover rounded-2xl" />
                            <p className="absolute bottom-0 left-0 right-0 bg-black/50 text-white text-center p-1 font-semibold rounded-b-2xl">
                                {selectedHotel?.name}
                            </p>
                        </div> 
                    ) : (
                        <div className="w-full p-4 flex flex-col items-center justify-center">
                            <h1 className="text-md font-semibold">No hotel selected yet</h1>
                            <p className="text-sm text-center">Choose a hotel from the list to get started</p>
                        </div>
                    )}
                </div>
                <div className="w-full flex items-center justify-between gap-2">
                    <div className="w-1/2">
                        <div className="w-full h-full flex items-center justify-start p-2">
                            <img src={calenderSVG} alt="Calendar" className="w-6 h-6" />
                            <h1 className="text-md ml-2">Check-in</h1>
                        </div>
                        <input type="date" value={checkInDate} onChange={(e) => setCheckInDate(e.target.value)} className="w-full p-2 bg-[#E8F5F5] text-black border border-[#558282] rounded-full hover:cursor-pointer" />
                    </div>
                    <div className="w-1/2">
                        <div className="w-full h-full flex items-center justify-start p-2">
                            <img src={calenderSVG} alt="Calendar" className="w-6 h-6" />
                            <h1 className="text-md ml-2">Check-out</h1>
                        </div>
                        <input type="date" value={checkOutDate} onChange={(e) => setCheckOutDate(e.target.value)} className="w-full p-2 bg-[#E8F5F5] text-black border border-[#558282] rounded-full hover:cursor-pointer" />
                    </div>
                </div>
                <p className="text-sm text-[#558282] w-full text-center">{totalNights > 0 ? `${totalNights} night${totalNights === 1 ? '' : 's'} selected` : 'Select check-in and check-out dates'}</p>
                <div className="p-2 flex gap-2">
                    <img src={doubleSVG} className="w-6 h-6" />
                    <h1>Guests</h1>
                </div>
                <div className="w-full flex items-center justify-between font-bold">
                    <button onClick={() => setGuestCount(guestCount > 1 ? guestCount - 1 : 1)} className="w-10 h-10 bg-[#0E7490] text-white p-2 rounded-full hover:bg-[#0891B2] transition-transform duration-200 ease-in-out hover:scale-105 hover:cursor-pointer">-</button>
                    <span>{guestCount}</span>
                    <button onClick={() => setGuestCount(guestCount + 1)} className="w-10 h-10 bg-[#0E7490] text-white p-2 rounded-full hover:bg-[#0891B2] transition-transform duration-200 ease-in-out hover:scale-105 hover:cursor-pointer">+</button>
                </div>
                <InputBox icon={promoSVG} label="Promo Code" placeholder="Enter promo code" buttonText="Redeem" value={promoCode} onClick={setPromoCode} />
                <button  className="w-full h-15 p-2 bg-linear-to-r from-[#0E7490] to-[#0E7490] text-white font-black rounded-full hover:to-[#06B6D3] hover:cursor-pointer">Confirm Reservation</button>
            </div>
        </div>
    )
}