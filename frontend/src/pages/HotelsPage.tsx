import PromoBanner from "../components/promotions/PromoBanner"
import RoomGrid from "../components/hotels/RoomGrid"
import PageTitle from "../components/common/PageTitle"
import RoomFilterBar from "../components/hotels/RoomFilterBar"

export default function Main() {
    return (
        <div className="relative w-full h-full bg-[#F0FAFA] px-6 py-4 flex flex-col gap-4 mt-16">
            <PromoBanner />
            <PageTitle title="Island Hotel Stays" description="Choose your perfect retreat — beachfront villas, garden bungalows, and ocean suites await." />
            <RoomFilterBar />
            <RoomGrid />
        </div>
    )
}