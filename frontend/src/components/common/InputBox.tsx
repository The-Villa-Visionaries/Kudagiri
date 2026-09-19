import downSVG from "../../assets/icons/justButt.svg"
import React from "react";

interface InputBoxProps {
    icon?: string;
    label: string;
    placeholder: string;
    buttonText?: string;
    value?: string;
    onClick?: () => void;
}

export default function InputBox({ icon, label, placeholder, buttonText, value, onClick }: InputBoxProps) {
    const [dropdownOpen, setDropdownOpen] = React.useState(false)
    buttonText = buttonText
    return (
        <div className="w-full flex flex-col">
            <div onClick={() => setDropdownOpen(!dropdownOpen)} className="p-2 flex gap-2 hover:cursor-pointer">
                {icon && <img src={icon} className="w-6 h-6" />}
                <h1>{label}</h1>
                <img src={downSVG} className={"w-6 h-6 ml-auto " + (dropdownOpen ? "rotate-180" : "")} />
            </div>
            {dropdownOpen && (
            <div className="w-full flex gap-2">
                <input type="text" placeholder={placeholder} value={value} className="w-2/3 p-2 px-3 bg-[#E8F5F5] text-black border border-[#558282] rounded-full" />
                {buttonText && <button onClick={onClick} className="w-1/3 p-2 bg-[#0E7490] text-white rounded-full hover:bg-[#0891B2] transition-transform duration-200 ease-in-out hover:scale-105 hover:cursor-pointer">{buttonText}</button>}
            </div>
            )}
        </div>
    )
}