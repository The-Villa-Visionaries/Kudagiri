interface CardRowProps {
    title: string;
    attribute: string;
}

export default function CardRow({ title, attribute }: CardRowProps) {
    return (
        <div className="flex items-center justify-between w-full px-3">
            <h1 className="text-sm font-medium">{title}</h1>
            <p className="text-sm font-medium text-[#0E7490]">{attribute}</p>
        </div>
    )
}