import { useNavigate, useSearchParams } from "react-router-dom"
import Header from "../components/common/Header"
import PageIndex from "../components/common/PageIndex"
import PageTitle from "../components/common/PageTitle"
import FilterBar from "../components/common/FilterBar"
import { useEffect, useState } from "react"
import FerryGrid from "../components/ferry/FerryGrid"
import Edit from "../components/ferry/Edit"
import Create from "../components/ferry/Create"

export default function Main() {
    const navigation = useNavigate();
    const [searchParams] = useSearchParams()
    const [switchState, setSwitchState] = useState(true)

    const role = searchParams.get("role") || "Visitor"
    const allowAccess = role === "Admin" || role === "Ferry-Operator"
    useEffect(() => {
        if (!allowAccess) {
            navigation("/ferry")
        }
    }, [allowAccess, navigation])

    const title = "Manage Ferry Routes"
    const description = "Verify guest eligibility, issue transit passes, and manage route timetables"
    const [ferry, setFerry] = useState([])
    const userId = 1

    useEffect(() => {
        async function fetchFerryPage() {
            try {
                const response = await fetch('http://localhost:8000/api/ferry', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ requestId: userId })
                });
                if (response.ok) {
                    const data = await response.json()
                    setFerry(data.ferry)
                }
            } catch (error) {
                console.error('Error loading page:', error)
            }
        }
        fetchFerryPage()
    }, [])
    return (
        <div className="relative w-full h-full bg-[#F0FAFA] bg-[radial-gradient(#4bc0ad_1px,transparent_1px)] [background-size:16px_16px] px-9 py-4 flex flex-col gap-4 mt-16">
            <Header />
            <PageTitle title={title} description={description} />
            <FilterBar Page="Ferry" Create={true} onCreateClick={() => setSwitchState(true)} />
            <div className="w-full flex items-start justify-between">
                <div className="min-w-4/6">
                    <FerryGrid role={role} edit={true} onClick={() => setSwitchState(false)} ferry={ferry} />
                    <PageIndex />
                </div>
                {switchState ? <Create /> : <Edit />}
            </div>
        </div>
    )
}