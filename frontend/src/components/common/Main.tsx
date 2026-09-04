import Advertisement from "../advert/Advertisement";
import RoomsGrid from "../hotels/RoomsGrid";
import PageTitle from "./PageTitle";
import Search from "./Search";

export default function Main() {
    return (
        <div className="relative w-full h-screen bg-[#F0FAFA] px-6 py-4 flex flex-col gap-4 mt-16">
            <Advertisement />
            <PageTitle title="Island Hotel Stays" description="Choose your perfect retreat — beachfront villas, garden bungalows, and ocean suites await." />
            <Search />
            <RoomsGrid />
        </div>
    )
}