import CardRow from "../common/CardRow";
import ticketSVG from "../../assets/icons/ticket.svg"
import InputBox from "../common/InputBox";

export default function Validation() {
    return (
        <div className="sticky top-19 w-full rounded-2xl bg-white overflow-hidden mt-9">
            <div className="w-full h-25 bg-linear-to-r from-[#0E7490] to-[#06B6D3] flex flex-col justify-center gap-2 p-4 text-white">
                <h1 className="text-lg font-black">Ticket Code</h1>
                <p className="text-sm pl-2">Enter the customer's ticket code to log their usage</p>
            </div>
            <div className="w-full p-4 flex flex-col gap-4">
                <div className="w-full border-dashed border-[#E8F5F5] border-3 rounded-2xl flex flex-col items-center justify-center p-4 text-[#558282]">
                    <h1 className="text-md font-semibold">No Route selected yet</h1>
                    <p className="text-sm text-center">Choose a Route from the list to get started</p>
                </div>
                <div className="w-full flex flex-col gap-3">
                    <InputBox icon={ticketSVG} label="Generate a Ticket" placeholder="Ticket code" buttonText="Generate & Print" value="AO_291748" />
                    <InputBox icon={ticketSVG} label="Ticket Code" placeholder="Enter ticket code" buttonText="Search" />
                    <CardRow title="Nausheen" attribute="Using 1 Ticket" />
                    <CardRow title="Livaa" attribute="Using 1 Ticket" />
                    <CardRow title="Other" attribute="Using 18 Ticket" />
                    <hr />
                    <div className="flex items-center justify-between w-full px-3">
                        <h1 className="text-lg font-bold">Visitors On Board</h1>
                        <p className="text-2xl font-bold text-[#0E7490]">20</p>
                    </div>
                    <button className="w-full h-15 p-2 bg-linear-to-r from-[#0E7490] to-[#0E7490] text-white font-black rounded-full hover:to-[#06B6D3] hover:cursor-pointer">Start</button>
                </div>
            </div>
        </div>
    )
}