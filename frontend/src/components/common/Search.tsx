import ArrowUpDown from '../../assets/icons/ArrowUpDown.svg'

export default function Search() {
    return (
        <div className="mx-5.5 bg-white border-[#C0E4E4] border-2 rounded-[35px] px-5 py-3 gap-5">
            <div className="flex items-center gap-3 flex-1">
                <div className="flex-1 h-10 border rounded-2xl border-[#C0E4E4] bg-[#E8F5F5] flex items-center justify-start px-3 gap-3">
                    <input type="text" placeholder='Search rooms by name or feature...' className="bg-transparent w-full h-full border-none focus:outline-none placeholder:text-[#558282]"/>
                </div>
                <img src={ArrowUpDown} alt="Arrow Up Down" className="w-5 h-5"/>
                <div className="w-50 h-10 border rounded-2xl border-[#C0E4E4] bg-[#E8F5F5] flex items-center justify-start px-3 gap-3">
                    <p className="text-[#558282]">Recommended</p>
                </div>
            </div>
            <div className="flex items-center gap-3 mt-3">
                <button className="bg-[#E8F5F5] text-[#558282] px-3 py-1 rounded-full hover:bg-[#0E7490] hover:text-white">🛏️ All rooms</button>
                <button className="bg-[#E8F5F5] text-[#558282] px-3 py-1 rounded-full hover:bg-[#0E7490] hover:text-white">🏖️ Beachfront</button>
                <button className="bg-[#E8F5F5] text-[#558282] px-3 py-1 rounded-full hover:bg-[#0E7490] hover:text-white">🌊 Ocean Suite</button>
                <button className="bg-[#E8F5F5] text-[#558282] px-3 py-1 rounded-full hover:bg-[#0E7490] hover:text-white">🌿 Garden</button>
                <button className="bg-[#E8F5F5] text-[#558282] px-3 py-1 rounded-full hover:bg-[#0E7490] hover:text-white">👨‍👩‍👧 Family</button>
            </div>
        </div>
    )
}