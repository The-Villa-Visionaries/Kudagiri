import { useSearchParams } from "react-router-dom"
import Header from "../components/common/Header"
import PageIndex from "../components/common/PageIndex"
import PageTitle from "../components/common/PageTitle"
import FilterBar from "../components/common/FilterBar"
import EventsBanner from "../components/promotions/EventsBanner"
import ThemeGrid from "../components/theme-park/ThemeGrid"
import Cart from "../components/theme-park/Cart"
import Validation from "../components/theme-park/Validation"

export default function Main() {
    const [searchParams, setSearchParams] = useSearchParams()

    const role = searchParams.get("role") || "Visitor"
    const allowAccess = role === "Admin" || role === "Ticketing-Staff"

    const title = allowAccess ? "Staff Activity & Event Validation" : "Theme Park Activities & Events"
    const description = allowAccess ? "Search activities, verify guest access, and redeem ticket codes to log usage." : "Browse activities, check availability, and book tickets for your next adventure."
    const sideBar = allowAccess ? <Validation /> : <Cart />
    return (
        <div className="relative w-full h-full bg-[#F0FAFA] bg-[radial-gradient(#4bc0ad_1px,transparent_1px)] [background-size:16px_16px] px-9 py-4 flex flex-col gap-4 mt-16">
            <Header />
            {!allowAccess && (<EventsBanner />)}
            <PageTitle title={title} description={description} />
            <FilterBar Page="Theme Park" />
            <div className="w-full flex items-start justify-between">
                <div className="min-w-4/6">
                    <ThemeGrid role={role} />
                    <PageIndex />
                </div>
                {sideBar}
            </div>
        </div>
    )
}