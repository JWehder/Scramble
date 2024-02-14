import GalleryPhoto from "../../../Utils/components/GalleryPhoto";
import EllipsisButton from "./EllipsisButton";

export default function Article({ data }) {
    return (
            <div className="flex hover:bg-gray-700 p-3 rounded-md w-[400px] h-[80px]">
                <div className="flex items-center justify-center">
                    <GalleryPhoto imgUrl={""} caption="julia wehder" />
                </div>

                <div className="truncate p-1">
                    <h1 className="text-base font-bold">
                        {data.title}
                    </h1>
                    
                    <p className="ml-1 text-left truncate p-1">
                        {data.caption}
                    </p>
                </div>


                <EllipsisButton />
            </div>
    )
}