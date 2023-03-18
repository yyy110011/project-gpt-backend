import React, { useState, useEffect } from "react";
import axios from "axios";
import ChatButtons from "../Atoms/ChatButtons";
import Button from "react-bootstrap/Button";
import ListGroup from "react-bootstrap/ListGroup";

const ChatLists: React.FC = () => {
  const [response, setResponse] = useState<any>("");
  const alertClicked = () => {
    alert("You clicked the third ListGroupItem");
  };
  useEffect(() => {
    // declare the data fetching function
    const fetchData = async () => {
      try {
        const res = await axios.get("http://localhost:8000/v1/get_chats/0");
        setResponse(res.data);
        console.log(res.data);
      } catch (err) {
        console.error(err);
      }
    };
    // call the function
    fetchData()
      // make sure to catch any error
      .catch(console.error);
  }, []);

  return (
    <ListGroup defaultActiveKey="#link1">
      <ListGroup.Item action href="#link1">
        Link 1
      </ListGroup.Item>
      <ListGroup.Item action href="#link2" disabled>
        Link 2
      </ListGroup.Item>
      <ListGroup.Item action onClick={alertClicked}>
        This one is a button
      </ListGroup.Item>
    </ListGroup>
  );
};

export default ChatLists;
