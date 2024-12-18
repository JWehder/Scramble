import React from 'react';
import { useState } from 'react';
import SquigglyUnderline from "../../Utils/components/SquigglyLine"
import Schedule from '../../Periods/components/Schedule';
import LeaguesList from "./LeaguesList"
import Button from '../../Utils/components/Button';
import PlayerPage from '../../Golfers/components/player/PlayerPage';
import { useDispatch, useSelector } from 'react-redux';
import { AppDispatch, RootState } from '../../../store';
import Modal from '../../Utils/components/Modal';
import { resetSelectedGolfer } from '../../Golfers/state/golferSlice';
import { useQueryClient } from '@tanstack/react-query';

export default function Dashboard() {
    const queryClient = useQueryClient();

    const [activeComponent, setActiveComponent] = useState("Schedule");

    const dispatch = useDispatch<AppDispatch>();

    const selectedGolfer = useSelector((state: RootState) => state.golfers.selectedGolfer);

    const onClose = () => {
        dispatch(resetSelectedGolfer());
        queryClient.invalidateQueries({ queryKey: ['golferTournamentDetails'] });
    };

    return (
        <div className='flex justify-center items-center w-full flex-col min-w-[700px]'>
            <div className='flex-row h-16 w-11/12 mb-5 flex items-center text-light font-PTSans'>
                <div className='w-1/3 flex items-center justify-center'>
                    <h1 className='text-xl lg:text-4xl md:text-2xl sm:text-xl'>
                        Dashboard
                    </h1>
                </div>

                <div className='p-5 flex items-center justify-center w-1/3'>
                        <SquigglyUnderline 
                        items={[{name:"Schedule"}, {name: "Leagues"}]}
                        setActiveComponent={setActiveComponent}
                        active={activeComponent}
                        />
                </div>
                <div className='w-1/3 flex items-center justify-center'>
                    <Button
                    type={null}
                    onClick={null}
                    size= 'md'
                    variant= 'secondary'
                    disabled={false}
                    >
                        Settings
                    </Button>
                </div>

            </div>
                <div className='w-10/12 rounded-lg overflow-auto spy-3 flex-grow shrink flex-row h-full max-h-[calc(100vh-225px)]'> 

                    { activeComponent === "Schedule" && 
                        <div className='flex items-center justify-center'>
                            <Schedule />
                        </div>
                    }
                    { activeComponent === "Leagues" && 
                        <div className='flex items-center justify-center'>
                            <LeaguesList />
                        </div>
                    }
                    { selectedGolfer ?
                        <Modal 
                        open={open} 
                        onClose={onClose} 
                        bgColor="dark-green"
                        closeButtonColor={'light'}
                        >
                        <div className="w-full h-auto flex items-center justify-center min-w-[900px]">
                            <div className="w-[90%] p-4 bg-middle rounded-xl transition-all duration-300 ease-in-out">
                                <PlayerPage />
                            </div>
                        </div>
                        </Modal>
                        :
                        ""
                    }
                </div>
        </div>
    );
  }