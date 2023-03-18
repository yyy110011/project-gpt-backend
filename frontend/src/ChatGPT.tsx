import React, { useState } from 'react';
import axios from 'axios';

const ChatGPT: React.FC = () => {
  const [message, setMessage] = useState<string>('');
  const [response, setResponse] = useState<string>('');

  const handleSendMessage = async () => {
    try {
      const res = await axios.post('http://localhost:8000/v1/chat/', {
        'user_id': "0",
        "user_name": "test1",
        "chat_id": "0",
        'message': message 
      });
      setResponse(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div>
      <h1>ChatGPT</h1>
      <input type="text" value={message} onChange={(e) => setMessage(e.target.value)} />
      <button onClick={handleSendMessage}>Send</button>
      {response && (
        <div>
          <p>{response}</p>
        </div>
      )}
    </div>
  );
};

export default ChatGPT;