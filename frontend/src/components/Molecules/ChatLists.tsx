import React, { useState, useEffect } from "react";
import axios from "axios";
import ChatButtons from "../Atoms/ChatButtons";
import Button from "react-bootstrap/Button";
import ListGroup from "react-bootstrap/ListGroup";

const ChatLists: React.FC = () => {
  const [response, setResponse] = useState<any>("");
  const alertClicked = () => {
    console.log("You clicked the third ListGroupItem");
  };
  useEffect(() => {
    // declare the data fetching function
    const fetchData = async () => {
      try {
        const res = await axios.get("http://localhost:8000/v1/get_chats/0");
        setResponse(res.data);
      } catch (err) {
        console.error(err);
      }
    };
    // call the function
    fetchData()
      // make sure to catch any error
      .catch(console.error);
  }, []);
  console.log(response);
  return (
    <div>
      <ListGroup defaultActiveKey="#link1">
        {Array.isArray(response.chats) &&
          response.chats.map((items: string, index: number) => {
            return (
              <ListGroup.Item
                action
                href={`#link${index}`}
                key={index}
                onClick={alertClicked}
              >
                {items}
              </ListGroup.Item>
            );
          })}
      </ListGroup>
    </div>
  );
};

export default ChatLists;
