import { useSelector } from 'react-redux';
import SignedOutHome from "./SignedOutHome";
import SignedInHome from './SignedInHome';

export default function Home() {

    const signedIn = useSelector((state) => state.users.user);

    return (
        <div className='w-full bg-dark h-full'>
            {
                signedIn ?
                <SignedInHome />
                :
                <SignedOutHome />
            }
        </div>
    )
}

