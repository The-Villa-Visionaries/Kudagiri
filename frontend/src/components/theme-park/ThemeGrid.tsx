import ThemeCard from "./ThemeCard"

interface themePark {
    themeParkId: number
    name: string
    description: string
    price: number
    rating: number
    reviews: number
    capacity: number
    duration: string
    location: string
    ageLimit: string
    image: string
}

interface ThemeGridProps {
    role?: string
    edit?: boolean
    onClick?: () => void
    themePark?: themePark[]
}

export default function ThemeGrid({ role, edit, onClick, themePark }: ThemeGridProps) {
    const totalThemeParks = themePark?.length || 0
    return (
        <div className="mr-5.5">
            <div className="flex items-center justify-between mb-4 mx-5">
                <p className="text-[#558282] text-sm bg-[#F0FAFA]"><span className="font-bold">{totalThemeParks}</span> Theme Park Activities and Events</p>
                <p className="text-[#558282] text-sm bg-[#F0FAFA]">Showing: 1-10</p>
            </div>
            <div className="flex flex-wrap gap-5 justify-between">
                {themePark?.map((theme, index) => (
                    <ThemeCard key={index} role={role} edit={edit} onClick={onClick} themePark={theme} />
                ))}
            </div>
        </div>
    )
}