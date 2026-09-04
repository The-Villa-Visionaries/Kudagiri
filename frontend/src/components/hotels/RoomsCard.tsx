import starIcon from '../../assets/Star.svg';
import bedIcon from '../../assets/Bed.svg';
import twoguestIcon from '../../assets/TwoGuest.svg';
import roomsizeIcon from '../../assets/RoomSize.svg';

export default function RoomsCard() {
    return (
        <div className="w-[calc(50%-50px)] bg-white rounded-2xl shadow-md overflow-hidden">
            <div className="relative w-full h-48 overflow-hidden">
                <img src="https://five-star-alliance.s3.amazonaws.com/field/image/nodes/2017/45956/0_villa-G.jpg" alt="Room" className="w-full h-48 object-cover transition-transform duration-500 ease-in-out hover:scale-110 active:scale-95"/>
            </div>
            <div className="p-4"> 
                <div className="flex items-center justify-between mb-2">
                    <h3 className="text-lg font-medium text-[#333]">Deluxe Room</h3>
                    <div className="flex items-center text-[#558282] text-sm">
                        <img src={starIcon} alt="Room" className="w-6 h-6 inline-block mr-1"/>
                        <p className="font-medium leading-[14px]"><span className="font-bold text-black">5</span> (312 reviews)</p>
                    </div>
                </div>
                <p className="text-[#558282]">Perfect for a romantic getaway</p>
                <div className="flex items-center gap-3 mt-1"> 
                    <div className="mr-1 flex items-center gap-1 mt-2">
                        <img src={twoguestIcon} alt="Guest" className="w-5 h-5 inline-block"/>
                        <p className="text-[#558282] text-sm">Upto 2 guests</p>
                    </div>
                    <div className="mr-1 flex items-center gap-1 mt-2">
                        <img src={roomsizeIcon} alt="Room Size" className="w-5 h-5 inline-block"/>
                        <p className="text-[#558282] text-sm">95 m²</p>
                    </div>
                    <div className="mr-1 flex items-center gap-1 mt-2">
                        <img src={bedIcon} alt="Bed" className="w-5 h-5 inline-block"/>
                        <p className="text-[#558282] text-sm">1 King Bed</p>
                    </div>
                </div>
                <div className="flex items-center gap-2 mt-3">
                    <div className="bg-[#E8F5F5] text-white p-1 px-2 rounded-full">
                        <p className="text-[#558282] text-sm">Plunge Pool</p>
                    </div>
                    <div className="bg-[#E8F5F5] text-white p-1 px-2 rounded-full">
                        <p className="text-[#558282] text-sm">Glass Floor Panel</p>
                    </div>
                    <div className="bg-[#E8F5F5] text-white p-1 px-2 rounded-full">
                        <p className="text-[#558282] text-sm">Butler Service</p>
                    </div>
                    <div className="bg-[#E8F5F5] text-white p-1 px-2 rounded-full">
                        <p className="text-[#558282] text-sm">WiFi</p>
                    </div>
                    <div className="bg-[#E8F5F5] text-white p-1 px-2 rounded-full">
                        <p className="text-[#558282] text-sm">+2 more</p>
                    </div>
                </div>
                <div className="bg-[#FFFBEB] border border-[#FDE998] text-white p-1 px-2 rounded-full mt-2 w-fit">
                    <p className="text-[#B6570F] text-sm font-medium">Only a few left — Get em while their hot!</p>
                </div>
                <hr className="border-[#E8F5F5] border-y-1 my-3" />
                <div className="flex items-center justify-between">
                    <div className="flex items-end">
                        <h3 className="text-2xl font-bold text-[#558282]">$780</h3>
                        <p className="text-[#558282] text-sm">/night</p>
                    </div>
                    <button className="bg-[#0E7490] text-white px-4 py-2 rounded-full font-bold hover:bg-[#0891B2] transition-transform duration-200 ease-in-out hover:scale-105 active:scale-95">Book Now</button>
                </div>
            </div>
        </div>
    )
}