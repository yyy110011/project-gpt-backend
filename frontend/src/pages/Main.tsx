import React from 'react'
import ChatGPT from '../components/Organisms/ChatGPT';
import ChatLists from '../components/Molecules/ChatLists';

const Main: React.FC  = () => {


    return (
        <div className='row'>
            <div className='col-sm-4'><ChatLists/></div>
            <div className='col-sm-8'> <ChatGPT /></div>  
        </div>
    )
}

export default Main;