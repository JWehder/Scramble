import Avatar from "../../../Utils/components/Avatar";
import PropTypes from 'prop-types';
import EllipsisButton from "./EllipsisButton";

export default function Message({ data }) {
    return (
        <div className="flex hover:bg-gray-700 p-2 rounded-md w-[250px] h-[80px]">
            <div>
                <Avatar size={"14"} imgUrl={""} name="user 1"/>
            </div>
            
            <p className="ml-1 overflow-hidden text-ellipsis w-[175px] p-1 text-left">
                {data}
            </p>

            <EllipsisButton />

        </div>
    )
}

Message.propTypes = {
    message: PropTypes.string.isRequired
}