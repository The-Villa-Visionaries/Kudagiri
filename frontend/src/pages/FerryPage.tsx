import Header from "../components/common/Header"
import EventBanner from "../components/promotions/EventsBanner"
import PageTitle from "../components/common/PageTitle"
import FilterBar from "../components/common/FilterBar"
import PageIndex from "../components/common/PageIndex"
import FerryGrid from "../components/ferry/FerryGrid"
import Cart from "../components/ferry/Cart"
import { useEffect, useState } from "react"
import { useNavigate, useSearchParams } from "react-router-dom"
import Validation from "../components/ferry/Validation"

export default function Main() {
    const navigation = useNavigate();
    const [searchParams] = useSearchParams()

    const role = searchParams.get("role") || "Visitor"
    const allowAccess = role === "Admin" || role === "Ferry-Operator"
    useEffect(() => {
        if (!allowAccess) {
            navigation("/ferry")
        }
    }, [allowAccess, navigation])

    const title = "Ferry Routes"
    const description = "Book your island transit — smooth ferry trips, seaplanes, and direct routes await"
    const sideBar = allowAccess ? <Validation /> : <Cart />
    return (
        <div className="relative w-full h-full bg-[#F0FAFA] bg-[radial-gradient(#4bc0ad_1px,transparent_1px)] [background-size:16px_16px] px-9 py-4 flex flex-col gap-4 mt-16">
            <Header />
            <EventBanner />
            <PageTitle title={title} description={description} />
            <FilterBar Page="Ferry" />
            <div className="w-full flex items-start justify-between">
                <div className="min-w-4/6">
                    <FerryGrid role={role} />
                    <PageIndex />
                </div>
                {sideBar}
            </div>
        </div>
    )
}