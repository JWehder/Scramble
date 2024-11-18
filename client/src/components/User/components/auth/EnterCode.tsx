import React, { useState, useEffect, FormEvent } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import Button from '../../../Utils/components/Button';
import NotificationBanner from '../../../Utils/components/NotificationBanner';
import {
  verifyEmail,
  resendCode,
  clearResendCodeError,
  clearVerifyEmailError
} from '../../state/userSlice';
import { AppDispatch, RootState } from '../../../../store' // Update with the correct path to your store
import LoadingWidget from '../../../Utils/components/LoadingWidget';

export default function VerifyEmail({ setResetPasswordEmail } : {setResetPasswordEmail: (email: string) => void}) {

  const dispatch = useDispatch<AppDispatch>();

  const [email, setEmail] = useState<string>('');
  const [code, setCode] = useState<string>('');
  const [timer, setTimer] = useState<number>(60);
  const [codeExpired, setCodeExpired] = useState<boolean>(false);

  const resendCodeError = useSelector((state: RootState) => state.users.resendCodeError);
  const resendCodeStatus = useSelector((state: RootState) => state.users.resendCodeStatus);
  const verifyEmailError = useSelector((state: RootState) => state.users.verifyEmailError);
  const showCode = useSelector((state: RootState) => state.users.showCode);

  const showCodeExpired = () => {
    setCodeExpired(true);
  };

  // Reset the timer when resendCodeStatus changes to idle and showCode is true
  useEffect(() => {
    if (resendCodeStatus === 'idle' && showCode) {
      setTimer(60); // Reset the timer
      setCodeExpired(false); // Reset the expired flag
      dispatch(clearResendCodeError()); // Clear errors
    }
  }, [showCode, resendCodeStatus]);

  // Handle countdown timer
  useEffect(() => {
    if (showCode && timer > 0) {
      const countdown = setInterval(() => {
        setTimer((prev) => prev - 1);
      }, 1000);

      return () => clearInterval(countdown);
    } else if (timer <= 0) {
      showCodeExpired(); // Mark the code as expired
    }
  }, [timer, showCode]);

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();


    dispatch(verifyEmail({ code, email }));

    setResetPasswordEmail(email)
  };

  const handleRequestClick = () => {
    dispatch(clearVerifyEmailError());
    dispatch(resendCode(email));
  };

  return (
    <div className="text-light font-PTSans rounded px-8 pt-6 pb-8 mb-4 w-full h-full">
      <h1 className="text-2xl text-center mb-4">Verify Your Email</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        {showCode && (
          <>
            {codeExpired ? (
              <NotificationBanner
                message="Your code has expired. Please request another with your email."
                variant="warning"
                timeout={10000}
                onClose={null}
              />
            ) : (
              <NotificationBanner
                message="Please check your email for your unique code"
                variant="success"
                timeout={10000}
                onClose={null}
              />
            )}
          </>
        )}

        <div className="mb-4">
          <label className="block text-sm font-bold mb-2" htmlFor="email">
            Email
          </label>
          <input
            className="shadow appearance-none border w-full py-2 px-3 leading-tight focus:outline-none focus:shadow-outline text-dark bg-light focus:ring-middle focus:border-middle rounded-full"
            id="email"
            type="text"
            placeholder="Please enter the email you signed up with"
            value={email}
            onChange={(e) => {
              if (resendCodeError || verifyEmailError) {
                dispatch(clearResendCodeError());
                dispatch(clearVerifyEmailError());
              }
              setEmail(e.target.value);
            }}
          />
        </div>

        {codeExpired && (
          <p className="text-red-500 font-bold text-sm italic">
            Your code expired. Please request a new one.
          </p>
        )}

        {showCode && timer > 0 && (
          <div className="mb-4">
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
                }
                setCode(e.target.value);
              }}
            />
          </div>
        )}

        {((verifyEmailError || resendCodeError)) && (
          <p className="text-red-500 font-bold text-sm italic">
            {verifyEmailError as React.ReactNode || resendCodeError as React.ReactNode}
          </p>
        )}

        <div className="flex items-center justify-between">
          {timer > 0 && showCode && (
            <Button 
            variant="secondary" 
            type="submit"
            onClick={null}
            disabled={false}
            size='md'
            >
              Submit Code
            </Button>
          )}
          {timer > 0 && showCode ? (
            <p className={`text-sm ${timer < 10 ? "text-red-500" : "text-light"}`}>Time remaining: {timer}s</p>
          ) : (
            null
          )}
        </div>

        <div className="mt-4 flex items-center space-x-2">
          <p
            className="font-bold text-sm cursor-pointer"
            onClick={handleRequestClick}
          >
            {showCode ? 'Request a New Code' : 'Request a Code'}
          </p>
          {resendCodeStatus === 'pending' && <LoadingWidget message="" />}
        </div>
      </form>
    </div>
  );
}
