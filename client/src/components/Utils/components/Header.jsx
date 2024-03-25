import { useDispatch } from 'react-redux';
import { setLoginModal } from '../../User/state/userSlice';
import Button from './Button';
import { useSelector } from 'react-redux';

export default function Header({ setShowLogin }) {
    const dispatch = useDispatch();

    function handleSignUpClick() {
        dispatch(setLoginModal(true));
        dispatch(setShowLogin(false));
    };

    function handleLoginClick() {
        dispatch(setLoginModal(true));
        dispatch(setShowLogin(true));
    };

    function handleGetTheAppClick() {

    };

    const isSignedIn = useSelector((state) => state.users.user)

    return (
        <div className="fixed top-0 w-full z-35 mb-1 bg-dark shadow-lg">
        <div className="p-0.5 bg-custom-gradient" />
            <div className="flex justify-center p-2">
            <div className="flex justify-between items-center w-full px-4">
                {/* First div */}
                <div className="flex-grow w-1/3" />

                {/* Second div */}
                <div className="flex justify-center items-center w-1/3">
                    <h1 className="text-3xl lg:text-5xl md:text-5xl sm:text-3xl font-lobster text-center bg-gradient-to-r from-green-700 via-green-300 to-teal-300 text-transparent bg-clip-text">
                        Scramble
                    </h1>
                </div>

                {/* Third div */}
                <div className="flex space-x-4 w-1/3">
                {isSignedIn ? 
                    ""
                    :
                    <>
                    <Button
                    variant="primary"
                    onClick={handleSignUpClick}
                    >
                        Sign Up
                    </Button>
                    <Button
                    variant="primary"
                    onClick={handleLoginClick}
                    >
                        Login
                    </Button>
                    </>
                }
                    <Button
                    variant="primary"
                    onClick={handleGetTheAppClick}
                    >
                        Get the App
                    </Button>
                </div>
            </div>
            </div>
        </div>
    )
}