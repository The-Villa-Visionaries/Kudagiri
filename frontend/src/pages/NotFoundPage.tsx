import { useEffect } from "react";
import { useNavigate } from "react-router-dom"
import Header from "../components/common/Header";

export default function Redirect() {
    const navigate = useNavigate()
    
    useEffect(() => {
        const timer = setTimeout(() => {
            navigate("/hotels", { replace: true })
        }, 3000);
        return () => clearTimeout(timer);
    }, [navigate]);

    return (
        <div className="relative w-screen h-screen bg-[#F0FAFA] bg-[radial-gradient(#4bc0ad_1px,transparent_1px)] [background-size:16px_16px]">
            <Header />
            <div className="w-full h-full flex items-center justify-center">
                <div className="w-1/3 bg-white p-8 rounded-lg shadow-md flex flex-col items-center gap-4">
                    <h1 className="text-2xl font-bold text-[#0E7490]">404 Error</h1>
                    <p className="text-[#0E7490] text-center">You might have mistyped the address or the page may have moved. Redirecting...</p>
                </div>
            </div>
        </div>
    )
}