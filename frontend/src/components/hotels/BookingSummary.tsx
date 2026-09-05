import calenderSVG from "../../assets/icons/calendar.svg"
import doubleSVG from "../../assets/icons/double.svg"
import promoSVG from "../../assets/icons/promo-d.svg"

export default function BookingSummary() {
    return (
        <div className="sticky top-22 w-full rounded-2xl bg-white overflow-hidden mt-8 shadow-md">
            <div className="w-full h-25 bg-linear-to-r from-[#0E7490] to-[#06B6D3] flex flex-col justify-center gap-2 p-4 text-white">
                <h1 className="text-lg font-black">Your Booking Summary</h1>
                <p className="text-sm pl-2">Complete the details below to reserve</p>
            </div>
            <div className="w-full p-4 flex flex-col gap-4">
                <div className="w-full border-dashed border-[#E8F5F5] border-3 rounded-2xl flex flex-col items-center justify-center p-4 text-[#558282]">
                    <h1 className="text-md font-semibold">No room selected yet</h1>
                    <p className="text-sm">Choose a room from the list to get started</p>
                </div>
                <div className="w-full flex items-center justify-between gap-2">
                    <div className="w-1/2">
                        <div className="w-full h-full flex items-center justify-start p-2">
                            <img src={calenderSVG} alt="Calendar" className="w-6 h-6" />
                            <h1 className="text-md ml-2">Check-in</h1>
                        </div>
                        <input type="date" className="w-full p-2 bg-[#E8F5F5] text-black border border-[#558282] rounded-full" />
                    </div>
                    <div className="w-1/2">
                        <div className="w-full h-full flex items-center justify-start p-2">
                            <img src={calenderSVG} alt="Calendar" className="w-6 h-6" />
                            <h1 className="text-md ml-2">Check-out</h1>
                        </div>
                        <input type="date" className="w-full p-2 bg-[#E8F5F5] text-black border border-[#558282] rounded-full" />
                    </div>
                </div>
                <p className="text-sm text-[#558282] w-full text-center">67 nights selected</p>
                <div className="p-2 flex gap-2">
                    <img src={doubleSVG} className="w-6 h-6" />
                    <h1>Guests</h1>
                </div>
                <div className="w-full flex items-center justify-between font-bold">
                    <button className="w-10 h-10 bg-[#0E7490] text-white p-2 rounded-full">-</button>
                    <span>2</span>
                    <button className="w-10 h-10 bg-[#0E7490] text-white p-2 rounded-full">+</button>
                </div>
                <div className="p-2 flex gap-2">
                    <img src={promoSVG} className="w-6 h-6" />
                    <h1>Promo Code</h1>
                </div>
                <div className="w-full flex gap-2">
                    <input type="text" placeholder="Enter promo code" className="w-2/3 p-2 px-3 bg-[#E8F5F5] text-black border border-[#558282] rounded-full" />
                    <button className="w-1/3 p-2 bg-[#0E7490] text-white rounded-full">Apply</button>
                </div>
                <button className="w-full h-15 p-2 bg-linear-to-r from-[#0E7490] to-[#0E7490] text-white font-black rounded-full hover:to-[#06B6D3]">Confirm Reservation</button>
                <p className="text-sm text-[#558282] w-full text-center px-4">Free cancellation up to 24 hours before check-in. Secure payments.</p>
            </div>
        </div>
    )
}