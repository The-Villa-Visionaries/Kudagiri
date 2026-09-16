import PromoBanner from "../components/promotions/PromoBanner"
import RoomGrid from "../components/hotels/RoomGrid"
import PageTitle from "../components/common/PageTitle"
import RoomFilterBar from "../components/hotels/RoomFilterBar"
import PageIndex from "../components/common/PageIndex"
import BookingSummary from "../components/hotels/BookingSummary"
import Header from "../components/common/Header"

export default function Main() {
    return (
        <div className="relative w-full h-full bg-[#F0FAFA] bg-[radial-gradient(#4bc0ad_1px,transparent_1px)] [background-size:16px_16px] px-9 py-4 flex flex-col gap-4 mt-16">
            <Header />
            <PromoBanner />
            <PageTitle title="Island Hotel Stays" description="Choose your perfect retreat — beachfront villas, garden bungalows, and ocean suites await." />
            <RoomFilterBar />
            <div className="w-full flex items-start justify-between">
                <div className="min-w-4/6">
                    <RoomGrid />
                    <PageIndex />
                </div>
                <BookingSummary />
            </div>
        </div>
    )
}