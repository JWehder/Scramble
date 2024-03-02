import React from 'react';
import Button from './Utils/components/Button';
import Standings from './Standings';

export default function Dashboard() {
    return (
      <div className="w-full h-screen pt-20 pb-16 px-6">
        <div>
          <div className='w-full flex justify-center items-center flex-col'>
            <div className='flex-row h-16 w-11/12 mb-5'>
              {/* ... */}
            </div>
            <div className='w-10/12 bg-light rounded-lg overflow-auto max-h-[500px]'> 
              <div className='border-b-black p-5 flex items-center justify-center'>
                <Button variant="primary" size="md">
                  League
                </Button>
                <Button>
                  Team
                </Button>
              </div>
              <div className='flex items-center justify-center'>
                <Standings />
              </div>
            </div>
          </div>
          <div>
            {/* ... */}
          </div>
        </div>
      </div>
    );
  }