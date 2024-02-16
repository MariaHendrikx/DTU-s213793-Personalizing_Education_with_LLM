import React, { useState, useEffect } from "react";
import axios from "axios";
import { Card } from "react-bootstrap";
import io from "socket.io-client"; // Make sure to import io

const RightPanel = () => {
  const [termsToLearnGoal, setTermsToLearnGoal] = useState({
    title: "Basic vocabulary and Personal Pronouns",
    words: [
      "wo",
      "ni",
      "ta",
      "women",
      "nimen",
      "tamen",
      "mei ge ren",
      "ni hao",
      "xiexie",
      "shi de",
      "bu",
      "qing",
      "pengyou",
      "jiao",
      "zaijian",
      "xihuan",
      "hao",
      "shi",
      "xuesheng",
    ],
  });

  const [termsExplained, setTermsExplained] = useState([]);
  const baseURLExplainer = "http://127.0.0.1:5001";

  useEffect(() => {
    const socket = io(baseURLExplainer);

    socket.on("update_withoutloading", () => {
      fetchTermsExplained();
    });

    fetchTermsExplained();

    return () => socket.disconnect();
  }, []);

  const fetchTermsExplained = async () => {
    try {
      const response = await axios.get(`${baseURLExplainer}/termsexplainedwithoutloading`);
      setTermsExplained(response.data.data);
    } catch (error) {
      console.error("Error fetching terms explained:", error);
    }
  };

  const [unlearnedTerms, setUnlearnedTerms] = useState([]);

  const compareWords = () => {
    const explainedWords = termsExplained.map((term) => term.word.toLowerCase());
    const unlearned = termsToLearnGoal.words.filter((word) => !explainedWords.includes(word.toLowerCase()));
    setUnlearnedTerms(unlearned);
  };

  useEffect(() => {
    compareWords();
  }, [termsExplained, termsToLearnGoal.words]);

  // Calculate learned terms
  const learnedTerms = termsToLearnGoal.words.filter((word) => !unlearnedTerms.includes(word));

  return (
    <div>
      <Card border="secondary" style={{ width: "18rem" }}>
        <Card.Header>Personal Info</Card.Header>
        <Card.Body>
          <Card.Title>Current Learning Objective</Card.Title>
          <Card.Text>{termsToLearnGoal.title}</Card.Text>
        </Card.Body>

        <Card.Body>
          <Card.Title>Terms To Learn</Card.Title>
          <div>
            <Card.Text>{termsToLearnGoal.words.join(", ")}</Card.Text>
          </div>
        </Card.Body>

        <Card.Body>
          <Card.Title>History</Card.Title>
          <Card.Text>
            <strong>Terms learned this session:</strong> {learnedTerms.join(", ")}
          </Card.Text>
          <Card.Text>
            <strong>Terms remaining:</strong> {unlearnedTerms.length > 0 ? unlearnedTerms.join(", ") : "All terms have been explained!"}
          </Card.Text>
          <Card.Text>
            <strong>Your status:</strong> Complete beginner
          </Card.Text>
        </Card.Body>
      </Card>
      <br />
    </div>
  );
};

export default RightPanel;
