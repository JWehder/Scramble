import GalleryPhoto from "../Utils/GalleryPhoto";

export default function News() {
    return (
        <div className="flex hover:bg-gray-700 p-2 rounded-md w-[400px] h-[80px] justify-center align-middle">
            <div>
                <GalleryPhoto imgUrl={""} caption="julia wehder" />
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