import calenderSVG from "../../assets/icons/calendar.svg"
import doubleSVG from "../../assets/icons/double.svg"
import InputBox from "../common/InputBox"
import promoSVG from "../../assets/icons/promo-d.svg"

export default function BookingSummary() {
    return (
        <div className="sticky top-19 w-full rounded-2xl bg-white overflow-hidden mt-9">
            <div className="w-full h-25 bg-linear-to-r from-[#0E7490] to-[#06B6D3] flex flex-col justify-center gap-2 p-4 text-white">
                <h1 className="text-lg font-black">Your Booking Summary</h1>
                <p className="text-sm pl-2">Complete the details below to reserve</p>
            </div>
            <div className="w-full p-4 flex flex-col gap-4">
                <div className="w-full border-dashed border-[#E8F5F5] border-3 rounded-2xl flex flex-col items-center justify-center p-4 text-[#558282]">
                    <h1 className="text-md font-semibold">No hotel selected yet</h1>
                    <p className="text-sm text-center">Choose a hotel from the list to get started</p>
                </div>
                <div className="w-full flex items-center justify-between gap-2">
                    <div className="w-1/2">
                        <div className="w-full h-full flex items-center justify-start p-2">
                            <img src={calenderSVG} alt="Calendar" className="w-6 h-6" />
                            <h1 className="text-md ml-2">Check-in</h1>
                        </div>
                        <input type="date" className="w-full p-2 bg-[#E8F5F5] text-black border border-[#558282] rounded-full hover:cursor-pointer" />
                    </div>
                    <div className="w-1/2">
                        <div className="w-full h-full flex items-center justify-start p-2">
                            <img src={calenderSVG} alt="Calendar" className="w-6 h-6" />
                            <h1 className="text-md ml-2">Check-out</h1>
                        </div>
                        <input type="date" className="w-full p-2 bg-[#E8F5F5] text-black border border-[#558282] rounded-full hover:cursor-pointer" />
                    </div>
                </div>
                <p className="text-sm text-[#558282] w-full text-center">67 nights selected</p>
                <div className="p-2 flex gap-2">
                    <img src={doubleSVG} className="w-6 h-6" />
                    <h1>Guests</h1>
                </div>
                <div className="w-full flex items-center justify-between font-bold">
                    <button className="w-10 h-10 bg-[#0E7490] text-white p-2 rounded-full hover:bg-[#0891B2] transition-transform duration-200 ease-in-out hover:scale-105 hover:cursor-pointer">-</button>
                    <span>2</span>
                    <button className="w-10 h-10 bg-[#0E7490] text-white p-2 rounded-full hover:bg-[#0891B2] transition-transform duration-200 ease-in-out hover:scale-105 hover:cursor-pointer">+</button>
                </div>
                <InputBox icon={promoSVG} label="Promo Code" placeholder="Enter promo code" buttonText="Redeem" />
                <button className="w-full h-15 p-2 bg-linear-to-r from-[#0E7490] to-[#0E7490] text-white font-black rounded-full hover:to-[#06B6D3] hover:cursor-pointer">Confirm Reservation</button>
            </div>
        </div>
    )
}