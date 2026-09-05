import RoomCard from "../hotels/RoomCard";

export default function RoomsGrid() {
    return (
        <div className="mx-5.5">
            <div className="flex items-center justify-between mb-4 mx-5">
                <p className="text-[#558282] text-sm"><span className="font-bold">67</span> rooms available</p>
                <p className="text-[#558282] text-sm">Showing: 1-10 of 67</p>
            </div>
            <div className="flex flex-wrap gap-5 justify-around">
                <RoomCard />
                <RoomCard />
                <RoomCard />
                <RoomCard />
            </div>
        </div>
    )
}