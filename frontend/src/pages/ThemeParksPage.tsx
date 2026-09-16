import Header from "../components/common/Header"
import PageTitle from "../components/common/PageTitle"

export default function Main() {
    return (
        <div className="relative w-full h-full bg-[#F0FAFA] bg-[radial-gradient(#4bc0ad_1px,transparent_1px)] [background-size:16px_16px] px-9 py-4 flex flex-col gap-4 mt-16">
            <Header />
            <PageTitle title="Events & Shows" description="Book your island adventures — from thrill rides to sunset shows and reef snorkels." />
        </div>
    )
}