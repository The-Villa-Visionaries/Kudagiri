import notificationSVG from "../../assets/icons/notification.svg"

export default function HeaderButtons() {
    return (
        <div className="w-10 flex items-center justify-center">
            <img src={notificationSVG} alt="Notification" className="w-7 h-7" />
        </div>     
    )
}
