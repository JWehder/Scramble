import React, { useState, useEffect } from 'react';
import Button from '../../../Utils/components/Button';
import { useDispatch } from 'react-redux';
import { verifyEmail, setShowLogin } from "../../state/userSlice";
import NotificationBanner from '../../../Utils/components/NotificationBanner';

export default function VerifyEmail() {
    const dispatch = useDispatch();

    const [code, setCode] = useState('');
    const [timer, setTimer] = useState(60);
    const [codeExpired, setCodeExpired] = useState(false);

    const showCodeExpired = () => {
        setCodeExpired(true);
    };
  
    // Handle countdown timer effect
    useEffect(() => {
        if (timer > 0) {
        const countdown = setInterval(() => {
            setTimer(timer - 1);
        }, 1000);
        return () => clearInterval(countdown);
        } else {
        showCodeExpired(); // Handle expired code scenario
        }
    }, [timer]);

    const handleSubmit = (e) => {
        e.preventDefault();

        dispatch(verifyEmail(code));
        dispatch(setShowLogin(true));
    };
  
    return (
      <div className="text-light font-PTSans rounded px-8 pt-6 pb-8 mb-4 w-full h-full">
        <h1 className="text-2xl text-center mb-4">Verify Your Email</h1>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            {
                codeExpired ?
                <NotificationBanner
                    message="Please check your email for your unique code"
                    variant="success"
                />
                :
                <NotificationBanner
                message="Your code has expired. Please request another"
                variant="warning"
                />
            }
            {
                incorrect
            }
            <label className="block text-sm font-bold mb-2" htmlFor="verification-code">
              Verification Code
            </label>
            <input
              className="shadow appearance-none border w-full py-2 px-3 leading-tight focus:outline-none focus:shadow-outline text-dark bg-light focus:ring-green-500 focus:border-green-500 rounded-full"
              id="verification-code"
              type="text"
              placeholder="Enter the code sent to your email"
              value={code}
              onChange={(e) => setCode(e.target.value)}
              disabled={codeExpired}
            />
          </div>
          <div className="flex items-center justify-between">
            <Button variant="secondary" type="submit">
              Submit Code
            </Button>
            {timer > 0 ? (
              <p className="text-sm text-light">Time remaining: {timer}s</p>
            ) : (
              <p className="text-sm text-red-500">Code expired</p>
            )}
          </div>
          <div className="mt-4">
            <p
              className="inline-block align-baseline font-bold text-sm text-light hover:text-middle cursor-pointer"
            >
              Request a New Code{' '}
              <a>
                Login
              </a>
            </p>
          </div>
        </form>
      </div>
    );
  }