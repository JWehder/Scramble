import React, { useState, useEffect } from 'react';
import Button from '../../../Utils/components/Button';
import { useDispatch, useSelector } from 'react-redux';
import { verifyEmail, resendCode, clearResendCodeError, clearVerifyEmailError } from "../../state/userSlice";
import NotificationBanner from '../../../Utils/components/NotificationBanner';

export default function VerifyEmail() {
    const dispatch = useDispatch();

    const [email, setEmail] = useState('');
    const [code, setCode] = useState('');
    const [timer, setTimer] = useState(60);
    const [codeExpired, setCodeExpired] = useState(false);

    const resendCodeError = useSelector((state) => state.users.resendCodeError);
    const resendCodeStatus = useSelector((state) => state.users.resendCodeStatus);
    const verifyEmailError = useSelector((state) => state.users.verifyEmailError)

    const showLogin = useSelector((state) => state.users.showLogin);

    const showCodeExpired = () => {
        setCodeExpired(true);
    };

    // Reset the timer when sendNewVerifyEmailCode is fulfilled
    useEffect(() => {
      if (resendCodeStatus === "idle") {
          setTimer(60); // Reset the timer when the email code is successfully sent
          setCodeExpired(false); // Reset the code expired flag
          dispatch(clearResendCodeError()); // Clear any error
      }
    }, [resendCodeStatus]);
  
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

        console.log(showLogin)

        dispatch(verifyEmail({
          code,
          email
        }));
    };
  
    return (
      <div className="text-light font-PTSans rounded px-8 pt-6 pb-8 mb-4 w-full h-full">
        <h1 className="text-2xl text-center mb-4">Verify Your Email</h1>
        <form onSubmit={handleSubmit} className='space-y-4'>
          {
              codeExpired ?
              <NotificationBanner
              message="Your code has expired. Please request another with your email."
              variant="warning"
              timeout={10000}
              />
              :
              <NotificationBanner
              message="Please check your email for your unique code"
              variant="success"
              timeout={10000}
              />
          }
          <div className='mb-4'>
            <label className="block text-sm font-bold mb-2" htmlFor="email">
              Email
            </label>
            <input
              className="shadow appearance-none border w-full py-2 px-3 leading-tight focus:outline-none focus:shadow-outline text-dark bg-light focus:ring-green-500 focus:border-green-500 rounded-full"
              id="email"
              type="text"
              placeholder="Please enter the email you signed up with"
              value={email}
              onChange={(e) => {
                if (resendCodeError || verifyEmailError) {
                  dispatch(clearResendCodeError());
                  dispatch(clearVerifyEmailError());
                };
                setEmail(e.target.value);
                
              }}
            />
          </div>
          { codeExpired && 
            <p className="text-red-500 font-bold text-sm italic">
              Please enter your email and select "request a new code" below to receive a new code.
            </p>
          }
          { !codeExpired && <div className="mb-4">
            <label className="block text-sm font-bold mb-2" htmlFor="verification-code">
              Verification Code
            </label>
            <input
              className="shadow appearance-none border w-full py-2 px-3 leading-tight focus:outline-none focus:shadow-outline text-dark bg-light focus:ring-green-500 focus:border-green-500 rounded-full"
              id="verification-code"
              type="text"
              placeholder="Enter the code sent to your email"
              value={code}
              onChange={(e) => {
                if (resendCodeError || verifyEmailError) {
                  dispatch(clearResendCodeError());
                  dispatch(clearVerifyEmailError());
                };
                setCode(e.target.value);
              }}
            />
          </div>
          }
          { (!codeExpired && (verifyEmailError || resendCodeError)) &&
            <p className="text-red-500 font-bold text-sm italic">
              {verifyEmailError || resendCodeError}
            </p>
          }

          <div className="flex items-center justify-between">
            { !codeExpired && <Button variant="secondary" type="submit">
              Submit Code
            </Button>
            }
            {timer > 0 ? (
              <p className="text-sm text-light">Time remaining: {timer}s</p>
            ) : (
              <p className="text-sm text-red-500">Code expired</p>
            )}
          </div>
          <div className="mt-4">
            <p
              className="inline-block align-baseline font-bold text-sm text-light hover:text-middle cursor-pointer"
              onClick={() => dispatch(resendCode(email))}
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