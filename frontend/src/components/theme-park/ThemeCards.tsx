import starSVG from "../../assets/icons/star.svg"
import RoomCardSpecs from "../hotels/RoomCardSpecs"
import clockSVG from "../../assets/icons/clock.svg"
import locationSVG from "../../assets/icons/location.svg"
import dangerSVG from "../../assets/icons/danger.svg"
import doubleSVG from "../../assets/icons/double.svg"
import justButtSVG from "../../assets/icons/justButt.svg"

export default function ThemeCards() {
    return (
        <div className="w-[calc(50%-20px)] bg-white rounded-2xl overflow-hidden group">
            <div className=" relative w-full h-48 overflow-hidden bg-linear-to-r from-[#0E7490] to-[#06B6D3]">
                <img src="https://www.travelandleisure.com/thmb/O8YmcAEEurVaI6ggOimGYUEOHBw=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/TAL-kings-island-MIDWESTCOASTERS0726-5da8f4d93b534a21ba9b9117d1c45a9e.jpg" alt="Theme Park" className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300 ease-in-out" />
            </div>
            <div className="p-4">
                <div className="flex items-center justify-between mb-2">
                    <h3 className="text-lg font-medium text-[#333]">Tsunami Surge Coaster</h3>
                    <div className="flex items-center text-[#558282] text-sm">
                        <img src={starSVG} alt="Room" className="w-6 h-6 inline-block mr-1"/>
                        <p className="font-medium leading-[14px]"><span className="font-bold text-black">4.67</span> (667 reviews)</p>
                    </div>
                </div>
                <p className="text-[#558282]">Perfect for a romantic getaway</p>
                <div className="flex flex-wrap items-center gap-3">
                    <p className="bg-[#FEF2F2]/50 border border-red text-[#BB1C1C] rounded-full px-3 font-bold">Extreme</p>
                    <RoomCardSpecs icon={clockSVG} text="4 min" />
                    <RoomCardSpecs icon={locationSVG} text="Thrill Zone, Sector A" />
                    <RoomCardSpecs icon={dangerSVG} text="Age 12+" />
                </div>
                <div className="w-full ">
                    <div className="flex items-center justify-between">
                        <div className="flex gap-2 text-[#558282]">
                            <img src={doubleSVG} className="w-6 h-6" />
                            <p>Today's Capacity</p>
                        </div>
                        <p className="text-[#BB1C1C] font-bold text-sm">289/320 booked (90%)</p>
                    </div>
                    <div className="w-full h-2 bg-[#E2F4F4] rounded-full mt-1">
                        <div className="w-[90%] h-full bg-[#BB1C1C] rounded-full" />
                    </div>
                </div>
                <div className="w-full mt-3 flex items-center justify-between">
                    <p className="text-[#558282]">View times & Book</p>
                    <img src={justButtSVG} className="w-6 h-6"/>
                </div>
                <hr className="border-[#E8F5F5] border-y my-3" />
                <div className="flex items-center justify-between mt-3">
                    <div className="flex items-end text-[#0E7490]">
                        <h3 className="text-2xl font-bold">from $28</h3>
                        <p className="text-sm">/person</p>
                    </div>
                    <button className="bg-[#0E7490] text-white px-4 py-2 rounded-full font-bold hover:bg-[#0891B2] transition-transform duration-200 ease-in-out hover:scale-105 hover:cursor-pointer">Book Now</button>
                </div>

            </div>
        </div>
    )
}