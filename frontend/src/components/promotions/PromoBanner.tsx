import promoSVG from "../../assets/icons/promo.svg"

export interface Promotion {
    name: string
    description: string
    offer: string
    fromDate: string
    toDate: string
    promoCode: string
}

interface PromoBannerProps {
    promo?: Promotion | null
}

export default function PromoBanner({ promo }: PromoBannerProps) {
    if (!promo) return null

    return (
        <div className="relative w-full bg-linear-to-r from-[#0E7490] to-[#06B6D3] flex items-center justify-between p-8 gap-5 rounded-2xl overflow-hidden z-10">
            <div className="absolute bottom-[3vh] left-[8vw] w-30 h-30 bg-[#2688A1] rounded-full z-11"/>
            <div className="absolute top-[3vh] right-[10vw] w-40 h-40 bg-[#20B6D1] rounded-full z-11"/>
            <div className="flex items-center gap-5 z-12">
                <img src={promoSVG} alt="Promotion" className="w-8 h-8 z-12"/>
                <p className="text-white z-12 text-lg">
                    <span className="font-bold text-shadow-lg">{promo.name} </span>
                    — {promo.offer} {promo.description} {promo.fromDate} – {promo.toDate}.
                    <span className="font-bold px-2 bg-white/30 rounded-full ml-2 text-shadow-none select-all">{promo.promoCode}</span>
                </p>
            </div>
        </div>
    )
}