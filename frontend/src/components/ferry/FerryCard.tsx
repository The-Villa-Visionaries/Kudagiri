import starSVG from "../../assets/icons/star.svg"
import RoomCardSpecs from "../hotels/RoomCardSpecs"
import clockSVG from "../../assets/icons/clock.svg"

interface Ferry {
    ferryId: number
    name: string
    description: string
    price: number
    duration: string
    rating: number
    reviews: number
    image: string
}

interface FerryCardProps {
    role?: string
    edit?: boolean
    onClick?: () => void
    ferry?: Ferry
}

export default function FerryCard({ role, edit, onClick, ferry }: FerryCardProps) {
    const allowAccess = role === "Admin" || role === "Ferry-Operator"
    let buttonText = allowAccess ? "Select" : "Book Now"
    buttonText = edit ? "Edit Route" : buttonText
    const imagePath = ferry?.image?.startsWith('/') ? ferry?.image : `/${ferry?.image}`
    const imgSrc = ferry?.image ? `http://localhost:8000${imagePath}` : ''
    return (
        <div className="w-[calc(50%-10px)] bg-white rounded-2xl overflow-hidden group">
            <div className="relative w-full h-48 overflow-hidden bg-linear-to-r from-[#0E7490] to-[#06B6D3]">
                <img src={imgSrc} className="w-full h-48 object-cover transition-transform duration-500 ease-in-out group-hover:scale-110 hover:cursor-pointer"/>
            </div>
            <div className="p-4"> 
                <div className="flex items-center justify-between mb-2">
                    <h3 className="text-lg font-medium text-[#333]">{ferry?.name}</h3>
                    <div className="flex items-center text-[#558282] text-sm">
                        <img src={starSVG} alt="Room" className="w-6 h-6 inline-block mr-1"/>
                        <p className="font-medium leading-[14px]"><span className="font-bold text-black">{ferry?.rating}</span> ({ferry?.reviews || 0} reviews)</p>
                    </div>
                </div>
                <p className="text-[#558282]">{ferry?.description}</p>
                <div className="flex flex-wrap items-center justify-between gap-3 mt-2">
                    <RoomCardSpecs icon={clockSVG} text={ferry?.duration.toString() ?? 'Unknown'} />
                </div>
                <hr className="border-[#E8F5F5] border-y-1 my-3" />
                <div className="flex items-center justify-between mt-2">
                    <div className="flex items-end text-[#0E7490]">
                        <h3 className="text-2xl font-bold">{ferry?.price}</h3>
                        <p className="text-sm">/way</p>
                    </div>
                    <button onClick={onClick} className="bg-[#0E7490] text-white px-4 py-2 rounded-full font-bold hover:bg-[#0891B2] transition-transform duration-200 ease-in-out hover:scale-105 hover:cursor-pointer">{buttonText}</button>
                </div>
            </div>
        </div>
    )
}