import FerryCard from "./FerryCard";

interface FerryGridProps {
    role?: string
    edit?: boolean
    onClick?: () => void
}

export default function FerryGrid({ role, edit, onClick }: FerryGridProps) {
    return (
        <div className="mr-5.5">
            <div className="flex items-center justify-between mb-4 mx-5">
                <p className="text-[#558282] text-sm bg-[#F0FAFA]"><span className="font-bold">99</span> Routes available</p>
                <p className="text-[#558282] text-sm bg-[#F0FAFA]">Showing: 1-10 of 99</p>
            </div>
            <div className="flex flex-wrap gap-5 justify-between">
                <FerryCard role={role} edit={edit} onClick={onClick} />
            </div>
        </div>
    )
}