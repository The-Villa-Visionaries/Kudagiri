import ThemeCards from "./ThemeCards"

export default function ThemeGrid() {
    return (
        <div className="mr-5.5">
            <div className="flex items-center justify-between mb-4 mx-5">
                <p className="text-[#558282] text-sm bg-[#F0FAFA]"><span className="font-bold">30</span> Theme Park Activities and Events</p>
                <p className="text-[#558282] text-sm bg-[#F0FAFA]">Showing: 1-10 of 30</p>
            </div>
            <div className="flex flex-wrap gap-5 justify-around">
                <ThemeCards />
                <ThemeCards />
                <ThemeCards />
                <ThemeCards />
            </div>
        </div>
    )
}