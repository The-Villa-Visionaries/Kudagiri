import HeaderButtons from "./HeaderButtons"
import Navigation from "./Navigation"
import Profile from "./Profile"
import { useNavigate } from "react-router-dom"

export default function Header() {
    const navigate = useNavigate();
    return (
        <div className="fixed top-0 left-0 right-0 px-7 w-full h-16 bg-white/80 backdrop-blur-[5px] flex items-center justify-between z-50 border-b border-[#C0E4E4]">
            <div className="flex items-center justify-start w-1/4 gap-2">
                <img src="https://static.vecteezy.com/system/resources/previews/057/689/164/large_2x/tropical-palm-trees-on-the-beach-at-sunset-vector.jpg" alt="Logo" className="h-8" />
                <p>KudaGiri</p>
            </div>
            <div className="flex items-center justify-center gap-4 w-2/4 h-full">
                <Navigation page="Hotels" onClick={() => navigate("/hotels")} />
                <Navigation page="Ferry" onClick={() => navigate("/ferry")} />
                <Navigation page="Theme Parks" onClick={() => navigate("/theme-parks")} />
            </div>
            <div className="flex items-center justify-end gap-2 w-1/4 h-full">
                <HeaderButtons />
                <HeaderButtons />
                <Profile />
            </div>
        </div>
    )
}