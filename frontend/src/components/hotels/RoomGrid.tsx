import RoomCard from "../hotels/RoomCard";

interface RoomGridProps {
    role?: string
    edit?: boolean
    onClick?: () => void
}

export default function RoomsGrid({ role, edit, onClick }: RoomGridProps) {
    return (
        <div className="mr-5.5">
            <div className="flex items-center justify-between mb-4 mx-5">
                <p className="text-[#558282] text-sm bg-[#F0FAFA]"><span className="font-bold">67</span> hotels available</p>
                <p className="text-[#558282] text-sm bg-[#F0FAFA]">Showing: 1-10 of 67</p>
            </div>
            <div className="flex flex-wrap gap-5 justify-between">
                <RoomCard role={role} edit={edit} onClick={onClick} />
                <RoomCard role={role} edit={edit} onClick={onClick} />
                <RoomCard role={role} edit={edit} onClick={onClick} />
                <RoomCard role={role} edit={edit} onClick={onClick} />
            </div>
        </div>
    )
}