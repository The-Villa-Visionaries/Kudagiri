interface PageTitleProps {
    title: string
    description?: string
}

export default function PageTitle({ title, description }: PageTitleProps) {
    return (
        <div className="mx-5.5">
            <h1 className="text-[2rem] font-bold w-fit bg-[#F0FAFA]">{title}</h1>
            {description && <p className="text-[#558282] w-fit bg-[#F0FAFA]">{description}</p>}
        </div>
    )
}