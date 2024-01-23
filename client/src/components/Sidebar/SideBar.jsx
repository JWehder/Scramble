import { GiGolfTee, GiGolfFlag } from "react-icons/gi";
import { BiMessage } from "react-icons/bi";
import { BiNews, BiSolidUser } from "react-icons/bi";
import SideIcon from "./SideIcon";

export default function SideBar() {
    return (
        <>
            <div className="fixed top-0 left-0 h-screen w-16 flex flex-col 
                            bg-gray-900 text-white shadow-lg">
                <div className="my-10" />
                <SideIcon icon={ <GiGolfFlag size="28" />} text="Leagues" />
                <SideIcon icon={<GiGolfTee size="28" />} text="Play"/>
                <SideIcon icon={<BiMessage size="28" />} text="Messages"/>
                <SideIcon icon={<BiNews size="28" />} text="News"/>
                <div 
                className= "fixed bottom-0 flex items-center justify-center"
                >
                    <SideIcon icon={<BiSolidUser size="28" />} />
                </div>
            </div>
        </>

    )

} 
