import { useNavigate } from "react-router-dom"
import naviButtSVG from "../../assets/icons/naviButt.svg"

export default function EventsBanner() {
    const navigate = useNavigate()

    const handleClick = () => {
        navigate("/theme-park?filter=beachevents")
    }
    return (
        <div className="group relative w-full h-70 bg-linear-to-r from-[#0E7490] to-[#06B6D3] rounded-2xl overflow-hidden z-10">
            <img src="https://assets.minorhotels.com/image/upload/q_auto,f_auto/media/minor/nh/images/nh-collection-maldives-havodda-resort/11_housereef/house_reef_image_1120x608_01.jpg" alt="Events Banner" className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300 ease-in-out" />
            <div className="absolute top-0 w-full">
                <button className="absolute left-0 w-15 h-70 flex items-center justify-center">
                    <img src={naviButtSVG} alt="Left Arrow" className="w-8 h-8 rounded-full bg-white/30 p-1 transition-transform duration-300 hover:scale-115 hover:cursor-pointer" />
                </button>
                <button className="absolute right-0 w-15 h-70 flex items-center justify-center">
                    <img src={naviButtSVG} alt="Right Arrow" className="w-8 h-8 rotate-180 rounded-full bg-white/30 p-1 transition-transform duration-300 hover:scale-115 hover:cursor-pointer" />
                </button>
            </div>
            <div className="absolute left-15 w-50% bottom-5 text-white">
                <p onClick={handleClick} className="rounded-full bg-white/30 text-sm p-1 px-3 w-fit my-1">🏖️ Beach Events</p>
                <h1 className="text-2xl font-black my-1">Discover the Reef</h1>
                <p className="text-md my-1">Guided snorkel and dive experiences in the island's protected marine sanctuary.</p>
                <button onClick={handleClick} className="bg-[#F97316] text-white text-sm py-2 px-4 rounded-full border border-transparent hover:bg-white hover:text-[#EA580C] hover:border hover:border-[#EA580C] font-black my-1 hover:cursor-pointer">Explore Beach Events</button>
            </div>

        </div>
    )
}