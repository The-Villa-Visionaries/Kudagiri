import { useNavigate, useLocation, useSearchParams } from "react-router-dom"

export default function PageIndex() {
    const navigate = useNavigate()
    const location = useLocation()
    const [searchParams] = useSearchParams()

    const handlePrevClick = () => {
        const currentPage = parseInt(searchParams.get("page") || "1", 10)
        if (currentPage <= 1) return
        navigate(`${location.pathname}?page=${currentPage - 1}`);
    }
    const handleNextClick = () => {
        let currentPage = parseInt(searchParams.get("page") || "1", 10)
        if (currentPage <= 0) {
            currentPage = 0
        }
        navigate(`${location.pathname}?page=${currentPage + 1}`)
    }
    const handlePageClick = (page:string) => {
        navigate(`${location.pathname}?page=${page}`)
    }
    return (
        <div className="w-full flex items-center justify-center gap-3 mt-5">
            <button onClick={handlePrevClick} className="rounded-full bg-white border border-[#0E7490] px-3 py-1 text-[#0E7490] transition-transform duration-200 ease-in-out hover:scale-105 hover:cursor-pointer">
                ← Prev
            </button>
            <div className="flex items-center justify-center gap-2">
                <button onClick={() => handlePageClick('1')} className="rounded-full aspect-square bg-[#0E7490] border border-transparent w-8 h-8 text-white">
                    1
                </button>
                <button onClick={() => handlePageClick('2')} className="rounded-full aspect-square bg-white border border-[#0E7490] w-8 h-8 text-[#0E7490]">
                    2
                </button>
            </div>
            <button onClick={handleNextClick} className="rounded-full bg-[#0E7490] border border-transparent px-3 py-1 text-white hover:bg-[#0891B2] transition-transform duration-200 ease-in-out hover:scale-105 hover:cursor-pointer">
                Next →
            </button>
        </div>
    )
}