import Avatar from "../Utils/Avatar";
import PropTypes from 'prop-types'

export default function Message({ message }) {
    return (
        <div className="flex hover:bg-gray-700 p-2 rounded-md w-[275px] h-[80px]">
            <div>
                <Avatar size={"14"} imgUrl={""} name="user 1"/>
            </div>
            
            <p className="ml-1 overflow-hidden text-ellipsis">What is up man hows it going spjfog osjrgiorni osngisncinrig nrshfiemigoneishg oienv irengho eingirenoin reingignorengibi einfoingireng fnoeignreongi rioegnierng</p>

            <div>
                <button className="text-gray-300 hover:text-white text-center justify-items-center align-center ml-2 top-0">
                    ...
                </button>
            </div>

        </div>
    )
}

Message.propTypes = {
    message: PropTypes.string.isRequired
}