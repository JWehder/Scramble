import TData from "../../../Utils/components/TData";
import THead from "../../../Utils/components/THead";
import range from "../../../Utils/methods/helpers";
import Birdie from "./Birdie";
import Bogey from "./Bogey";
import React from "react";

export default function HolesComparisonChart({ rounds } : { rounds: object }) {

    return (
        <div className="w-full flex-shrink p-2 border-y-2">
            <div className="flex flex-row p-2">
                <THead datapoint="Holes" />
                {
                    range(1,18,1).map((holeNumber) => {
                        return (
                            <THead datapoint={holeNumber} />
                        )
                    })
                }
            </div>
            <div className="flex flex-row p-2">
                <TData datapoint="Par" />
                {
                    range(1,18,1).map(() => {
                        let parNumber = Math.floor(Math.random() * 5) + 1;
                        return (
                            <TData datapoint={parNumber} />
                        )
                    })
                }
            </div>
            <div className="flex flex-row p-2">
                <TData datapoint="Strokes" />
                {
                    range(1,18,1).map((_, idx) => {
                        let parNumber = Math.floor(Math.random() * 5) + 1;
                        return (
                            <div className="flex-grow flex items-center justify-center w-8">   
                                <Birdie>
                                    <TData datapoint={parNumber} />
                                </Birdie>
                            </div>
                        )
                    })
                }
            </div>
            <div className="flex flex-row p-2">
                <TData datapoint="Ovr" />
                {
                    range(1,18,1).map(() => {
                        let parNumber = Math.floor(Math.random() * 5) + 1;
                        return (
                            <div className="flex-grow flex items-center justify-center w-8"> 
                                <Bogey size="12">
                                    <Bogey size="10">
                                        <Bogey size="8">
                                            <Bogey>
                                                <TData datapoint={-parNumber} />
                                            </Bogey>
                                        </Bogey>
                                    </Bogey>
                                </Bogey>    
                            </div>
                        )
                    })
                }
            </div>
            

        </div>
    )
}