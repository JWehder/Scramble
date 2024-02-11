import GalleryPhoto from "../Utils/GalleryPhoto";
import EllipsisButton from "./EllipsisButton";

export default function Article() {
    return (
            <div className="flex hover:bg-gray-700 p-3 rounded-md w-[400px] h-[80px]">
                <div className="flex items-center justify-center">
                    <GalleryPhoto imgUrl={""} caption="julia wehder" />
                </div>
                
                <p className="ml-1 text-left overflow-hidden text-ellipsis p-1">What is up man hows it going spjfog osjrgiorni osngisncinrig nrshfiemigoneishg oienv irengho eingirenoin reingignorengibi einfoingireng fnoeignreongi rioegnierng</p>

                <EllipsisButton />
            </div>
    )
}