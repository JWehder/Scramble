import { useDispatch } from 'react-redux';
import { setLoginModal } from '../../state/userSlice';
import { googleLogout } from '@react-oauth/google';

export default function User() {
    const dispatch = useDispatch();

    function logout() {
        dispatch(setLoginModal(true));
        googleLogout();
    };

    return (
        <div className="p-2 rounded-md justify-center align-middle">
            
            <div className="hover:bg-gray-700 text-center p-2 rounded-lg">
                Refer a friend
            </div>

            <div className="hover:bg-gray-700 text-center p-2 rounded-lg">
                Settings
            </div>

            <hr className="text-white m-1" />
            
            <div 
            className="hover:bg-gray-700 text-center p-2 rounded-lg"
            onClick={() => logout()}
            >
                Logout
            </div>

        </div>
    )
}