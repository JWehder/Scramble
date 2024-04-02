import Player1 from "../../../../assets/i-1.png";
import THead from "../../../Utils/components/THead";
import TData from "../../../Utils/components/TData";

export default function PlayerPageHeader() {

    const playerHeaders = ["Age", "Country", "PGA Debut", "Swings", "Weight", "College", "Events Played", "Cuts", "Cuts Made", "Earnings", "World Rank"]

    const playerInfo = {
        Age: 26,
        Country: "USA",
        pgaDebut: 2018,
        swings: "R",
        weight: 200,
        college: "University of Texas",
        eventPlayed: 6,
        cuts: 3,
        cutsMade: 2,
        earnings: "$72441",
        worldRank: 256
    };

    return (
        <div className="bg-middle w-full h-1/3 rounded-t-xl flex">
            <div className="w-1/4">
                <div className="flex items-center justify-center flex-grow">
                    <img src={Player1} alt="Player1" />
                </div>
            </div>
            <div className="w-3/4">
                <div className="flex items-center justify-center font-PTSans p-2 text-light">
                    <h1 className="text-2xl">Scottie Scheffler</h1>
                </div>
                <div className="text-light font-PTSans space-x-2 flex-col p-2">
                    <div className="flex-row flex">
                        {
                            Object.keys(playerInfo).slice(0, 5).map((key, idx) => {
                                return (
                                <THead datapoint={playerHeaders[idx]}>
                                    <TData datapoint={playerInfo[key] } />
                                </THead>
                                )
                            })
                        }
                    </div>
                    <div className="flex-row flex">
                        {
                            Object.keys(playerInfo).slice(5).map((key, idx) => {
                                return (
                                <THead datapoint={playerHeaders[idx + 5]}>
                                    <TData datapoint={playerInfo[key] }/>
                                </THead>
                                )
                            })
                        }
                    </div>
                </div>
            </div>
        </div>
    )
}