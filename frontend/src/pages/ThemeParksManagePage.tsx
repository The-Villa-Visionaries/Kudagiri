import { useNavigate, useSearchParams } from "react-router-dom"
import Header from "../components/common/Header"
import PageIndex from "../components/common/PageIndex"
import PageTitle from "../components/common/PageTitle"
import FilterBar from "../components/common/FilterBar"
import ThemeGrid from "../components/theme-park/ThemeGrid"
import Edit from "../components/theme-park/Edit"
import { useEffect, useState } from "react"
import Create from "../components/theme-park/Create"

export default function Main() {
    const navigation = useNavigate();
    const [searchParams] = useSearchParams()
    const [switchState, setSwitchState] = useState(true)

    const role = searchParams.get("role") || "Visitor"
    const allowAccess = role === "Admin" || role === "Ticketing-Staff"
    useEffect(() => {
        if (!allowAccess) {
            navigation("/theme-parks")
        }
    }, [allowAccess, navigation])

    const title = "Manage Theme Park Activities"
    const description = "Manage the activities available in your theme park. You can add, edit, or delete activities as needed."
    const [themePark, setThemePark] = useState([])
    const userId = 1

    useEffect(() => {
        async function fetchThemeParkPage() {
            try {
                const response = await fetch('http://localhost:8000/api/theme-park', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ requestId: userId })
                });
                if (response.ok) {
                    const data = await response.json()
                    setThemePark(data.themePark)
                }
            } catch (error) {
                console.error('Error loading page:', error)
            }
        }
        fetchThemeParkPage()
    }, [])
    return (
        <div className="relative w-full h-full bg-[#F0FAFA] bg-[radial-gradient(#4bc0ad_1px,transparent_1px)] [background-size:16px_16px] px-9 py-4 flex flex-col gap-4 mt-16">
            <Header />
            <PageTitle title={title} description={description} />
            <FilterBar Page="Theme Park" Create={true} onCreateClick={() => setSwitchState(true)} />
            <div className="w-full flex items-start justify-between">
                <div className="min-w-4/6">
                    <ThemeGrid role={role} edit={true} onClick={() => setSwitchState(false)} themePark={themePark} />
                    <PageIndex />
                </div>
                {switchState ? <Create /> : <Edit />}
            </div>
        </div>
    )
}