import React from "react";
import Eagle from "./Eagle";
import Birdie from "./Birdie";
import Bogey from "./Bogey";
import Albatross from "./Albatross";

export const ScoreWrapper = ({ score, children } : { score: number, children: React.ReactNode }) => {
    if (score === -2) {
        return <Eagle>{children}</Eagle>;
    } else if (score === -1) {
        return <Birdie>{children}</Birdie>;
    } else if (score === 1) {
        return <Bogey size="6">{children}</Bogey>;
    } else if (score === -3) {
        return <Albatross>{children}</Albatross>;
    } 
    return <div>{children}</div>; // Default case for par or other scores
};