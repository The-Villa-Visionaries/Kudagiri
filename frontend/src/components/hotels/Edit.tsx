import InputBox from "../common/InputBox"
import doubleSVG from "../../assets/icons/double.svg"
import roomSizeSVG from "../../assets/icons/room_size.svg"
import bedSVG from "../../assets/icons/bed.svg"

export default function Edit() {
    return (
        <div className="sticky top-19 w-full max-h-[89vh] rounded-2xl bg-white overflow-hidden mt-9">
            <div className="w-full h-25 bg-linear-to-r from-[#0E7490] to-[#06B6D3] flex flex-col justify-center gap-2 p-4 text-white">
                <h1 className="text-lg font-black">Edit Hotel</h1>
                <p className="text-sm pl-2">Edit the details of the selected hotel</p>
            </div>
            <div className="w-full p-4 flex flex-col gap-4">
                <div className="w-full border-dashed border-[#E8F5F5] border-3 rounded-2xl flex flex-col items-center justify-center p-4 text-[#558282]">
                    <h1 className="text-md font-semibold">No Hotel selected yet</h1>
                    <p className="text-sm text-center">Choose an Hotel from the list to get started</p>
                </div>
                <div className="w-full flex flex-col overflow-y-auto max-h-[46vh]">
                    <div className="w-full border-dashed border-[#E8F5F5] border-3 rounded-2xl flex flex-col items-center justify-center p-4 text-[#558282] hover:cursor-pointer">
                        <h1 className="text-md font-semibold">Upload Image</h1>
                    </div>
                    <InputBox label="Title" placeholder="Enter a title"/>
                    <InputBox label="Description" placeholder="Enter a description" />
                    <InputBox label="Price" placeholder="Enter a price" />
                    <InputBox icon={doubleSVG} label="Capacity" placeholder="Enter a capacity" />
                    <InputBox icon={roomSizeSVG} label="Room Size" placeholder="Enter a room size" />
                    <InputBox icon={bedSVG} label="Bed Type" placeholder="Enter a bed type" />
                    <InputBox label="Amenities" placeholder="Enter amenities seprated by coma" />
                    <InputBox label="Offer" placeholder="Enter offer" />
                </div>    
                <div className="w-full flex gap-2">
                    <button className="w-full h-15 p-2 bg-linear-to-r from-[#6B7280] to-[#6B7280] text-white font-black rounded-full hover:to-[#9CA3AF] hover:cursor-pointer">Cancel Edit</button>
                    <button className="w-full h-15 p-2 bg-linear-to-r from-[#0E7490] to-[#0E7490] text-white font-black rounded-full hover:to-[#06B6D3] hover:cursor-pointer">Save Edit</button>
                </div>
                <p className="text-sm text-center text-red-500 italic underline hover:cursor-pointer">Click here to delete this activity.</p>            
            </div>
        </div>
    )
}