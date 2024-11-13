import { useEffect } from "react";
import { useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom'; 
import HowToPlay from "./HowToPlay";
import GamesCarousel from "./GamesCarousel";
import Title from "./Title";
import AuthModal from "../auth/AuthModal";

export default function SignedOutHome() {
    const navigate = useNavigate();
  
    const signedIn = useSelector((state) => state.users.user);

    useEffect(() => {
        console.log("should be moving to leagues")
        if (signedIn) {
            navigate("/leagues");
        }
        
    }, [signedIn]);
  
    return (
      <div className="flex-grow">
        <Title />
        <HowToPlay />
        <GamesCarousel />
        <AuthModal />

      </div>
    );
  }