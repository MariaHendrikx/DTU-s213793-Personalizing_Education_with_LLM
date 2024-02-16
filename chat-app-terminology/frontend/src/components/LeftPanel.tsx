import React, { useState, useEffect } from "react";
import axios from "axios";
import { Card } from "react-bootstrap";
import io from "socket.io-client"; // Import Socket.IO client

const LeftPanel = () => {
  const [termsExplained, setTermsExplained] = useState([]);
  const baseURLExplainer = "http://127.0.0.1:5001"; // Your API base URL

  useEffect(() => {
    // Connect to Socket.IO server
    const socket = io(baseURLExplainer);

    // Listen for "update" event
    socket.on("update", () => {
      console.log("Data updated, fetching terms explained");
      fetchTermsExplained();
    });

    // Initial fetch
    fetchTermsExplained();

    return () => {
      socket.disconnect(); // Clean up on component unmount
    };
  }, []); // Empty dependency array means this effect runs only once on mount

  const fetchTermsExplained = async () => {
    try {
      const response = await axios.get(`${baseURLExplainer}/termsexplained`);
      setTermsExplained(response.data.data);
    } catch (error) {
      console.error("Error fetching terms explained:", error);
    }
  };


  return (
    <div>
      <Card border="secondary" style={{ width: "18rem" }}>
        <Card.Header>Vocabulary</Card.Header>

        <Card.Body style={{ padding: "0" }}>
          <Card.Title style={{ margin: "10px" }}>List</Card.Title>
          <div
            style={{
              height: "30vh", // Set the maximum height
              overflowY: "scroll", // Enable vertical scrolling
              padding: "10px",
            }}
          >
            {termsExplained.map((term, index) => (
              <div key={index} style={{ marginBottom: "5px" }}>
                <strong>{term.word}</strong>: {term.translation}
              </div>
            ))}
          </div>
        </Card.Body>

        <Card.Body style={{ padding: "0" }}>
          <Card.Title style={{ margin: "10px" }}>Explanations</Card.Title>
          <div
            style={{
              height: "40vh", // Set the maximum height
              overflowY: "scroll", // Enable vertical scrolling
              padding: "10px",
            }}
          >
            {termsExplained.map((term, index) => (
              <div key={index} style={{ marginBottom: "5px" }}>
                <strong>{term.word}</strong>: {term.explanation}
              </div>
            ))}
          </div>
        </Card.Body>

      </Card>
      <br />
    </div>
  );
};

export default LeftPanel;
