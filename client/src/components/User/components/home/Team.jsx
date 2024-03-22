import Button from "./Utils/components/Button";

export default function Team() {
    return (
        <div className='flex-row h-16 w-11/12 mb-5 pl-14 flex text-light font-PTSans'>
            <div className="flex-1 flex items-center">   
                <h1 className='text-4xl'>Team Name</h1>
            </div>
            
            <div className="flex-1 flex items-center justify-center">
                <div className="mr-2">
                    <Button 
                        variant="primary" 
                        size="md"
                    >
                        Trade
                    </Button>
                </div>


                <Button 
                    variant="primary" 
                    size="md"
                >
                    Waivers
                </Button>
            </div>
        </div>
    )
}