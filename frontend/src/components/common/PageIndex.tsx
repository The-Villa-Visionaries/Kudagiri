export default function PageIndex() {
    return (
        <div className="w-full flex items-center justify-center gap-3 mt-5">
            <button className="rounded-full bg-transparent border border-[#558282] px-3 py-1 text-[#95A0A0]">
                ← Prev
            </button>
            <div className="flex items-center justify-center gap-2">
                <button className="rounded-full bg-[#558282] border border-[#558282] px-3 py-1 text-white">
                    1
                </button>
                <button className="rounded-full bg-transparent border border-[#558282] px-3 py-1 text-[#95A0A0]">
                    2
                </button>
            </div>
            <button className="rounded-full bg-[#558282] border border-[#558282] px-3 py-1 text-white">
                Next →
            </button>
        </div>
    )
}