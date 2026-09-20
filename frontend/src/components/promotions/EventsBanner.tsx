import { useNavigate } from "react-router-dom"
import naviButtSVG from "../../assets/icons/naviButt.svg"
import { useEffect, useState } from "react"

interface Event {
    name: string
    description: string
    buttonText: string
    tag: string
    image: string
}

interface EventsBannerProps {
    events?: Event[]
}

export default function EventsBanner({ events }: EventsBannerProps) {
    if (!events || events.length === 0) return null
    const navigate = useNavigate()
    const [currentIndex, setCurrentIndex] = useState(0)
    const imagePath = events?.[currentIndex]?.image?.startsWith('/') ? events?.[currentIndex]?.image : `/${events?.[currentIndex]?.image}`
    const imgSrc = events?.[currentIndex]?.image ? `http://localhost:8000${imagePath}` : ''

    const handleClick = () => {
        navigate("/theme-park?filter=" + events?.[currentIndex]?.tag)
    }
    const handleBackClick = () => {
        setCurrentIndex((prevIndex) => (prevIndex - 1 + (events?.length || 1)) % (events?.length || 1))
    }
    const handleNextClick = () => {
        setCurrentIndex((prevIndex) => (prevIndex + 1) % (events?.length || 1))
    }

    useEffect(() => {
        const interval = setInterval(() => {
            setCurrentIndex((prevIndex) => (prevIndex + 1) % (events?.length || 1))
        }, 15000)
        return () => clearInterval(interval)
    }, [events?.length])
    return (
        <div className="group relative w-full h-70 bg-linear-to-r from-[#0E7490] to-[#06B6D3] rounded-2xl overflow-hidden z-10">
            <img src={imgSrc} alt="Events Banner" className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300 ease-in-out" />
            <div className="absolute top-0 w-full">
                <button onClick={handleBackClick} className="absolute left-0 w-15 h-70 flex items-center justify-center">
                    <img src={naviButtSVG} alt="Left Arrow" className="w-8 h-8 rounded-full bg-white/30 p-1 transition-transform duration-300 hover:scale-115 hover:cursor-pointer" />
                </button>
                <button onClick={handleNextClick} className="absolute right-0 w-15 h-70 flex items-center justify-center">
                    <img src={naviButtSVG} alt="Right Arrow" className="w-8 h-8 rotate-180 rounded-full bg-white/30 p-1 transition-transform duration-300 hover:scale-115 hover:cursor-pointer" />
                </button>
            </div>
            <div className="absolute left-15 w-50% bottom-5 text-white">
                <p onClick={handleClick} className="rounded-full bg-white/30 text-sm p-1 px-3 w-fit my-1">{events?.[currentIndex]?.tag}</p>
                <h1 className="text-2xl font-black my-1">{events?.[currentIndex]?.name}</h1>
                <p className="text-md my-1">{events?.[currentIndex]?.description}</p>
                <button onClick={handleClick} className="bg-[#F97316] text-white text-sm py-2 px-4 rounded-full border border-transparent hover:bg-white hover:text-[#EA580C] hover:border hover:border-[#EA580C] font-black my-1 hover:cursor-pointer">{events?.[currentIndex]?.buttonText}</button>
            </div>

        </div>
    )
}