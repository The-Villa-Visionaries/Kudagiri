import PromoCode from "../common/PromoCode";
import CardRow from "../common/CardRow";

export default function Cart() {
    return (
        <div className="sticky top-19 w-999 rounded-2xl bg-white overflow-hidden mt-9">
            <div className="w-full h-25 bg-linear-to-r from-[#0E7490] to-[#06B6D3] flex flex-col justify-center gap-2 p-4 text-white">
                <h1 className="text-lg font-black">Tickets</h1>
                <p className="text-sm pl-2">Complete the details below to reserve</p>
            </div>
            <div className="w-full p-4 flex flex-col gap-4">
                <div className="w-full border-dashed border-[#E8F5F5] border-3 rounded-2xl flex flex-col items-center justify-center p-4 text-[#558282]">
                    <h1 className="text-md font-semibold">No Route selected yet</h1>
                    <p className="text-sm text-center">Choose an Route from the list to get started</p>
                </div>
                <div className="w-full flex flex-col gap-4">
                    <PromoCode />
                    <CardRow title="Subtotal" attribute="$0.00" />
                    <CardRow title="Discount" attribute="-$10.00" />
                    <CardRow title="Tax (8%)" attribute="$0.00" />
                    <hr />
                    <div className="flex items-center justify-between w-full px-3">
                        <h1 className="text-lg font-bold">Total</h1>
                        <p className="text-2xl font-bold text-[#0E7490]">-$10.00</p>
                    </div>
                    <button className="w-full h-15 p-2 bg-linear-to-r from-[#0E7490] to-[#0E7490] text-white font-black rounded-full hover:to-[#06B6D3] hover:cursor-pointer">Checkout</button>
                </div>
            </div>
        </div>
    )
}