interface PageTitleProps {
    title: string
    description?: string
}

export default function PageTitle({ title, description }: PageTitleProps) {
    return (
        <div className="mx-5.5">
            <h1 className="text-[2rem] font-bold">{title}</h1>
            {description && <p className="text-[#558282]">{description}</p>}
        </div>
    )
}