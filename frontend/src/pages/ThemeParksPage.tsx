import Header from "../components/common/Header"
import PageIndex from "../components/common/PageIndex"
import PageTitle from "../components/common/PageTitle"
import RoomFilterBar from "../components/hotels/RoomFilterBar"
import EventsBanner from "../components/promotions/EventsBanner"
import ThemeCards from "../components/theme-park/ThemeCards"
import ThemeGrid from "../components/theme-park/ThemeGrid"

export default function Main() {
    return (
        <div className="relative w-full h-full bg-[#F0FAFA] bg-[radial-gradient(#4bc0ad_1px,transparent_1px)] [background-size:16px_16px] px-9 py-4 flex flex-col gap-4 mt-16">
            <Header />
            <EventsBanner />
            <PageTitle title="Events & Shows" description="Book your island adventures — from thrill rides to sunset shows and reef snorkels." />
            <RoomFilterBar />
            <div className="w-full flex items-start justify-between">
                <div className="min-w-4/6">
                    <ThemeGrid />
                    <PageIndex />
                </div>
            </div>
        </div>
    )
}