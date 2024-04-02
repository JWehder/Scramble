import THead from "../../../Utils/components/THead";
import range from "../../../Utils/methods/helpers";

export default function HolesComparisonChart() {

    return (
        <div className="w-full flex-shrink">
            <div className="flex flex-row">
                <THead datapoint="Holes" />
                {
                    range(1,18,1).map((holeNumber) => {
                        return (
                            <THead datapoint={holeNumber} />
                        )
                    })
                }
            </div>
            <div>
                
            </div>

        </div>
    )
}