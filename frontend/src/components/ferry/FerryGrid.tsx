import FerryCard from "./FerryCard";

interface Ferry {
    ferryId: number
    name: string
    description: string
    price: number
    duration: string
    rating: number
    reviews: number
    image: string
}

interface FerryGridProps {
    role?: string
    edit?: boolean
    onClick?: () => void
    ferry?: Ferry[]
}

export default function FerryGrid({ role, edit, onClick, ferry }: FerryGridProps) {
    const totalFerries = ferry?.length || 0
    return (
        <div className="mr-5.5">
            <div className="flex items-center justify-between mb-4 mx-5">
                <p className="text-[#558282] text-sm bg-[#F0FAFA]"><span className="font-bold">{totalFerries}</span> Routes available</p>
                <p className="text-[#558282] text-sm bg-[#F0FAFA]">Showing: 1-10</p>
            </div>
            <div className="flex flex-wrap gap-5 justify-between">
                {ferry?.map((ferry) => (
                    <FerryCard key={ferry.ferryId} role={role} edit={edit} onClick={onClick} ferry={ferry} />
                ))}
            </div>
        </div>
    )
}