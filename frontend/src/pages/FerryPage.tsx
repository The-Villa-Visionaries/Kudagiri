import Header from "../components/common/Header"
import EventBanner from "../components/promotions/EventsBanner"
import PageTitle from "../components/common/PageTitle"
import FilterBar from "../components/common/FilterBar"
import PageIndex from "../components/common/PageIndex"
import FerryGrid from "../components/ferry/FerryGrid"
import Cart from "../components/ferry/Cart"

export default function Main() {
    return (
        <div className="relative w-full h-full bg-[#F0FAFA] bg-[radial-gradient(#4bc0ad_1px,transparent_1px)] [background-size:16px_16px] px-9 py-4 flex flex-col gap-4 mt-16">
            <Header />
            <EventBanner />
            <PageTitle title="Island Ferry Routes & Schedules" description="Book your next voyage — reliable ferries, seaplanes, and rocketships await." />
            <FilterBar Page="Ferry" />
            <div className="w-full flex items-start justify-between">
                <div className="min-w-4/6">
                    <FerryGrid />
                    <PageIndex />
                </div>
                <Cart />
            </div>
        </div>
    )
}