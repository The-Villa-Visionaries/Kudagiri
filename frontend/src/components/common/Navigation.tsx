interface NavigationProps {
    page: string
    onClick?: () => void
}
export default function Navigation({ page, onClick }: NavigationProps) {
    return (
        <div className="px-3 h-full flex items-center gap-4 text-[#20B6D1] font-bold hover:border-b-3" onClick={onClick}>
            <h1>{page}</h1>
        </div>
    )
}