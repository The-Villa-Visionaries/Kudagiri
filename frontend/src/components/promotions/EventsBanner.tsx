import naviButtSVG from "../../assets/icons/naviButt.svg"

export default function EventsBanner() {
    return (
        <div className="relative w-full h-70 bg-linear-to-r from-[#0E7490] to-[#06B6D3] rounded-2xl overflow-hidden z-10">
            <img src="https://assets.minorhotels.com/image/upload/q_auto,f_auto/media/minor/nh/images/nh-collection-maldives-havodda-resort/11_housereef/house_reef_image_1120x608_01.jpg" alt="Events Banner" className="w-full h-full object-cover" />
            <div className="absolute top-1/2 w-full">
                <button className="absolute left-2 rounded-full bg-white/30 p-1">
                    <img src={naviButtSVG} alt="Left Arrow" className="w-8 h-8" />
                </button>
                <button className="absolute right-2 rounded-full bg-white/30 p-1">
                    <img src={naviButtSVG} alt="Right Arrow" className="w-8 h-8 rotate-180" />
                </button>
            </div>
            <div className="absolute left-15 w-50% bottom-5 text-white">
                <p className="rounded-full bg-white/30 text-sm p-1 px-3 w-fit my-1">🏖️ Beach Events</p>
                <h1 className="text-2xl font-black my-1">Discover the Reef</h1>
                <p className="text-md my-1">Guided snorkel and dive experiences in the island's protected marine sanctuary.</p>
                <button className="bg-[#F97316] text-white text-sm py-2 px-4 rounded-full border border-transparent hover:bg-white hover:text-[#EA580C] hover:border hover:border-[#EA580C] font-black my-1">Explore Water Events</button>
            </div>

        </div>
    )
}