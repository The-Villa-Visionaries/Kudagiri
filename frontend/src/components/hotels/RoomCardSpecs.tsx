interface RoomCardSpecsProps {
    icon: string
    text: string
}

export default function RoomCardSpecs({ icon, text }: RoomCardSpecsProps) {
    return (
        <div className="mr-1 flex items-center gap-1">
            <img src={icon} alt="Icon" className="w-5 h-5 inline-block"/>
            <p className="text-[#558282] text-sm">{text}</p>
        </div>
    )
}