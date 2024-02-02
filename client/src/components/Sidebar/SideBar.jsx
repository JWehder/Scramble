import { GiGolfTee, GiGolfFlag } from "react-icons/gi";
import { BiMessage } from "react-icons/bi";
import { BiNews, BiSolidUser } from "react-icons/bi";
import Tooltip from "../Utils/Tooltip";
import SidebarContent from "./SidebarContent";
import GlowingWrapper from "./GlowingWrapper";

export default function SideBar() {

    return (
        <>
            <div className="fixed top-0 left-0 h-screen w-16 flex flex-col bg-gray-900 text-white shadow-lg my-15">
                <div className="flex-grow flex flex-col items-center">
                    <div className="my-10" />
                    <div className="mt-2 mb-2">
                        <GlowingWrapper color = "green">
                        <Tooltip 
                        direction = "left"
                        icon = {<GiGolfFlag size="28" />}
                        sidebar
                        >
                            <SidebarContent type={"Leagues"} />
                        </Tooltip>
                        </GlowingWrapper>
                    </div>

                    <div className="mt-2 mb-2">
                        <GlowingWrapper color = "green">
                        <Tooltip 
                        icon = {<GiGolfTee size="28" />} 
                        direction = "left"
                        sidebar
                        >
                            <SidebarContent type={"Play"} />
                        </Tooltip> 
                        </GlowingWrapper>
                    </div>

                    <div className="mb-2 mt-2">
                        <GlowingWrapper color = "green">
                            <Tooltip 
                            icon = {<BiMessage size="28" />} 
                            direction = "left"
                            sidebar
                            >
                                <SidebarContent type={"Messages"} />
                            </Tooltip> 
                        </GlowingWrapper>
                    </div>

                    <div className="mb-2 mt-2">
                        <GlowingWrapper color = "green">
                        <Tooltip 
                        icon = {<BiNews size="28" />} 
                        direction = "left"
                        sidebar
                        >
                            <SidebarContent type={"News"} />
                        </Tooltip>
                        </GlowingWrapper>
                    </div>

                </div>
                <div className="flex items-center justify-center my-10">
                    <div className="mb-2 mt-2">
                        <GlowingWrapper color = "green">
                        <Tooltip 
                        icon = {<BiSolidUser size="28" />} 
                        direction = "left"
                        sidebar
                        >
                            <SidebarContent type={"User"} />
                        </Tooltip>
                        </GlowingWrapper>
                    </div>

                </div>
            </div>
        </>

    )

} 
