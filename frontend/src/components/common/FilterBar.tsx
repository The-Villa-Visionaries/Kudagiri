import sortSVG from "../../assets/icons/sort.svg"

interface FilterBarProps {
    Page: string
}

export default function FilterBar({ Page }: FilterBarProps) {
    let message = ""
    let PicksList = [""]

    if (Page === "Hotels") {
        message = "Search hotels by name or feature..."
        PicksList = [
            "🛏️ All Hotels",
            "🏖️ Beachfront",
            "🌊 Ocean Suite",
            "🌿 Garden",
            "🌴 Poolside",
            "👨‍👩‍👧 Family"
        ]
    } else if (Page === "Theme Park") {
        message = "Search activities by name or feature..."
        PicksList = [
            "🌴 All Activities",
            "🎢 Rides",
            "🎭 Shows",
            "🏖️ Beach Events",
            "🍽️ Dining",
            "🧸 Kids"
        ]
    } else if (Page === "Ferry") {
        message = "Search routes by name or feature..."
        PicksList = [
            "🌊 All Routes",
            "🚆 Train Routes",
            "🚤 Ferry Routes",
            "✈️ Seaplane Routes",
            "🚀 Rocketship Routes"
        ]
    }
    return (
        <div className="bg-white border-[#C0E4E4] border-2 rounded-2xl px-5 py-3 gap-5">
            <div className="flex items-center gap-3 flex-1">
                <div className="flex-1 h-10 border rounded-2xl border-[#C0E4E4] bg-[#E8F5F5] flex items-center justify-start px-3 gap-3">
                    <input type="text" placeholder={message} className="bg-transparent w-full h-full border-none focus:outline-none placeholder:text-[#558282]"/>
                </div>
                <img src={sortSVG} alt="Sort" className="w-5 h-5 hover:cursor-pointer"/>
                <div className="w-50 h-10 border rounded-2xl border-[#C0E4E4] bg-[#E8F5F5] flex items-center justify-start px-3 gap-3">
                    <p className="text-[#558282]">Recommended</p>
                </div>
            </div>
            <div className="flex items-center gap-3 mt-3">
                {PicksList.map((pick, index) => (
                    <button key={index} className="bg-[#E8F5F5] text-[#558282] px-3 py-1 rounded-full hover:bg-[#0E7490] hover:text-white hover:cursor-pointer">
                        {pick}
                    </button>
                ))}
            </div>
        </div>
    )
}