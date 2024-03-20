import SideBar from "./User/components/sidebar/SideBar";
import LeagueDashboard from "./LeagueDashboard";
import { Routes, Route } from "react-router-dom";

export default function SignedInHome() {
    return ( 
        <div className="w-full h-full pt-20 pb-16">
            
            <Routes>
                <Route exact path="/leagues/:id" element={LeagueDashboard} />
                <Route path="/leagues" element={}
            </Routes>
        </div>
    )
}