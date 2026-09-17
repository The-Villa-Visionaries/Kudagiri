import promoSVG from "../../assets/icons/promo-d.svg"

export default function PromoCode() {
    return (
        <div className="w-full flex flex-col">
            <div className="p-2 flex gap-2">
                <img src={promoSVG} className="w-6 h-6" />
                <h1>Promo Code</h1>
            </div>
            <div className="w-full flex gap-2">
                <input type="text" placeholder="Enter promo code" className="w-2/3 p-2 px-3 bg-[#E8F5F5] text-black border border-[#558282] rounded-full" />
                <button className="w-1/3 p-2 bg-[#0E7490] text-white rounded-full hover:bg-[#0891B2] transition-transform duration-200 ease-in-out hover:scale-105 hover:cursor-pointer">Apply</button>
            </div>
        </div>
    )
}