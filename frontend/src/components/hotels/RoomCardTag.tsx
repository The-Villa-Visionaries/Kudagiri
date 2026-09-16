interface RoomCardTagProps {
    text: string
}

export default function RoomCardTag({ text }: RoomCardTagProps) {
    return (
        <div className="bg-[#E8F5F5] text-white py-1 px-2 rounded-full h-7 truncate">
            <p className="text-[#558282] text-sm">{text}</p>
        </div>
    )
}