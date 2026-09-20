import starSVG from "../../assets/icons/star.svg"
import bedSVG from "../../assets/icons/bed.svg"
import doubleSVG from "../../assets/icons/double.svg"
import roomsizeSVG from "../../assets/icons/room_size.svg"
import RoomCardSpecs from "./RoomCardSpecs"
import RoomCardTag from "./RoomCardTag"

interface ThemeCardProps {
    role?: string
    edit?: boolean
    onClick?: () => void
}

export default function RoomsCard({ role, edit, onClick }: ThemeCardProps) {
    const allowAccess = role === "Admin" || role === "Hotel-Staff"
    let buttonText = allowAccess ? "Select" : "Book Now"
    buttonText = edit ? "Edit Hotel" : buttonText
    return (
        <div className="w-[calc(50%-10px)] bg-white rounded-2xl overflow-hidden group">
            <div className="relative w-full h-48 overflow-hidden bg-linear-to-r from-[#0E7490] to-[#06B6D3]">
                <img src="https://five-star-alliance.s3.amazonaws.com/field/image/nodes/2017/45956/0_villa-G.jpg" className="w-full h-48 object-cover transition-transform duration-500 ease-in-out group-hover:scale-110 hover:cursor-pointer"/>
            </div>
            <div className="p-4"> 
                <div className="flex items-center justify-between mb-2">
                    <h3 className="text-lg font-medium text-[#333]">Couples Retreat</h3>
                    <div className="flex items-center text-[#558282] text-sm">
                        <img src={starSVG} alt="Room" className="w-6 h-6 inline-block mr-1"/>
                        <p className="font-medium leading-[14px]"><span className="font-bold text-black">5</span> (312 reviews)</p>
                    </div>
                </div>
                <p className="text-[#558282]">Perfect for a romantic getaway</p>
                <div className="flex items-center gap-3">
                    <RoomCardSpecs icon={doubleSVG} text="Upto 2 guests" />
                    <RoomCardSpecs icon={roomsizeSVG} text="95 m²" />
                    <RoomCardSpecs icon={bedSVG} text="1 King Bed" />
                </div>
                <div className="flex items-center gap-2 mt-2">
                    <RoomCardTag text="Plunge Pool" />
                    <RoomCardTag text="Butler Service" />
                    <RoomCardTag text="WiFi" />
                    <RoomCardTag text="+2 more" />
                </div>
                <div className="bg-[#FFFBEB] border border-[#FDE998] text-white p-1 px-2 rounded-full mt-2 w-fit">
                    <p className="text-[#B6570F] text-sm font-medium">Only a few left — Get em while their hot!</p>
                </div>
                <hr className="border-[#E8F5F5] border-y-1 my-3" />
                <div className="flex items-center justify-between mt-2">
                    <div className="flex items-end text-[#0E7490]">
                        <h3 className="text-2xl font-bold">$780</h3>
                        <p className="text-sm">/night</p>
                    </div>
                    <button onClick={onClick} className="bg-[#0E7490] text-white px-4 py-2 rounded-full font-bold hover:bg-[#0891B2] transition-transform duration-200 ease-in-out hover:scale-105 hover:cursor-pointer">{buttonText}</button>
                </div>
            </div>
        </div>
    )
}