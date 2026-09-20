import starSVG from "../../assets/icons/star.svg"

interface FerryCardProps {
    role?: string
    edit?: boolean
    onClick?: () => void
}

export default function FerryCard({ role, edit, onClick }: FerryCardProps) {
    const allowAccess = role === "Admin" || role === "Ferry-Operator"
    let buttonText = allowAccess ? "Select" : "Book Now"
    buttonText = edit ? "Edit Route" : buttonText
    return (
        <div className="w-[calc(50%-10px)] bg-white rounded-2xl overflow-hidden group">
            <div className="relative w-full h-48 overflow-hidden bg-linear-to-r from-[#0E7490] to-[#06B6D3]">
                <img src="https://storage.ghost.io/c/26/7f/267f0e18-b0e6-4e7e-a5b1-41d5277633b4/content/images/wp-content/uploads/2021/07/how-rockets-work.jpg" className="w-full h-48 object-cover transition-transform duration-500 ease-in-out group-hover:scale-110 hover:cursor-pointer"/>
            </div>
            <div className="p-4"> 
                <div className="flex items-center justify-between mb-2">
                    <h3 className="text-lg font-medium text-[#333]">Deep Space Luxury</h3>
                    <div className="flex items-center text-[#558282] text-sm">
                        <img src={starSVG} alt="Room" className="w-6 h-6 inline-block mr-1"/>
                        <p className="font-medium leading-[14px]"><span className="font-bold text-black">4.99</span> (9,192 reviews)</p>
                    </div>
                </div>
                <p className="text-[#558282]">Float seamlessly beside panoramic glass walls framing the endless starfields. Drifting across interstellar highways toward your next galaxy has never felt more effortless</p>
                <hr className="border-[#E8F5F5] border-y-1 my-3" />
                <div className="flex items-center justify-between mt-2">
                    <div className="flex items-end text-[#0E7490]">
                        <h3 className="text-2xl font-bold">$0.01</h3>
                        <p className="text-sm">/way</p>
                    </div>
                    <button onClick={onClick} className="bg-[#0E7490] text-white px-4 py-2 rounded-full font-bold hover:bg-[#0891B2] transition-transform duration-200 ease-in-out hover:scale-105 hover:cursor-pointer">{buttonText}</button>
                </div>
            </div>
        </div>
    )
}