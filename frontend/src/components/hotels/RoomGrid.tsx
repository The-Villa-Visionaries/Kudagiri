import RoomCard from "../hotels/RoomCard"

interface Hotel {
    hotelId: number
    name: string
    description: string
    price: number
    rating: number 
    capacity: number
    roomSize: string
    bedType: string
    amenities: string
    offers: string
    image: string
}

interface RoomGridProps {
    role?: string
    edit?: boolean
    onClick?: () => void
    hotels: Hotel[]
}

export default function RoomsGrid({ role, edit, onClick, hotels }: RoomGridProps) {
    const totalHotels = hotels.length
    return (
        <div className="mr-5.5">
            <div className="flex items-center justify-between mb-4 mx-5">
                <p className="text-[#558282] text-sm bg-[#F0FAFA]"><span className="font-bold">{totalHotels}</span> hotels available</p>
                <p className="text-[#558282] text-sm bg-[#F0FAFA]">Showing: 1-10 of {totalHotels}</p>
            </div>
            <div className="flex flex-wrap gap-5 justify-between">
                {hotels.map((hotel, index) => (
                    <RoomCard key={index} role={role} edit={edit} onClick={onClick} hotels={hotel} />
                ))}
            </div>
        </div>
    )
}