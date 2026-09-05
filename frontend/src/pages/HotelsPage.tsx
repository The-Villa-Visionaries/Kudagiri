import PromoBanner from "../components/promotions/PromoBanner"
import RoomGrid from "../components/hotels/RoomGrid"
import PageTitle from "../components/common/PageTitle"
import RoomFilterBar from "../components/hotels/RoomFilterBar"
import PageIndex from "../components/common/PageIndex"
import BookingSummary from "../components/hotels/BookingSummary"

export default function Main() {
    return (
        <div className="relative w-full h-full bg-[#F0FAFA] px-6 py-4 flex flex-col gap-4 mt-16">
            <PromoBanner />
            <PageTitle title="Island Hotel Stays" description="Choose your perfect retreat — beachfront villas, garden bungalows, and ocean suites await." />
            <RoomFilterBar />
            <div className="w-full flex items-start justify-between">
                <div className="min-w-3/4">
                    <RoomGrid />
                    <PageIndex />
                </div>
                <BookingSummary />
            </div>
        </div>
    )
}