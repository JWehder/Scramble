import Avatar from "./Avatar";
import imgUrl from "../assets/i.png"

export default function Message() {
    return (
        <div className="flex hover:bg-gray-700 p-2 rounded-md w-[275px]">
            <Avatar imgUrl={imgUrl} name="user 1"/>
            <p className="ml-2 w-[200px] h-[100px] overflow-hidden text-ellipsis">What is up man hows it going spjfog osjrgiorni osngisncinrig nrshfiemigoneishg oienv irengho eingirenoin reingignorengibi einfoingireng fnoeignreongi rioegnierng</p>
            <button className="">...</button>
        </div>
    )
}