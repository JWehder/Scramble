import { useSelector } from 'react-redux';
import Button from './Button';

export default function HeaderButtons({ handleSignUpClick, handleLoginClick, handleGetTheAppClick }) {

    const isSignedIn = useSelector((state) => state.users.user);

    return (
        <div className="flex space-x-4 w-1/3 sm:text scale-0 sm:scale-0 md:scale-100 lg:scale-100 xl:scale-100">
            { isSignedIn ? 
                ""
                :
                <>
                    <Button
                    variant="primary"
                    size="md"
                    onClick={handleSignUpClick}
                    >
                        Sign Up
                    </Button>
                    <Button
                    variant="primary"
                    size="md"
                    onClick={handleLoginClick}
                    >
                        Login
                    </Button>
                </>
            }
            <Button
            variant="secondary"
            size="md"
            onClick={handleGetTheAppClick}
            >
                Get the App
            </Button>
        </div>
    )
}