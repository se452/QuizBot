import React, { useState } from "react";

const Home = () => {
  //state constants can be edited
  const [YoutubeLink, SetYoutubeLink] = useState(""); //to store link
  const [Transcript, SetTranscript] = useState(""); // to store transcript
  const [Quiz, SetQuiz] = useState(""); //to store quiz

  const submitRequest = () => {
    //handle api requests
    //for git commit
  };

  return (
    <div>
      <h1>Quiz Generator</h1>
      <input
        type="text"
        placeholder="Enter the Link"
        value={YoutubeLink}
        onChange={(e) => SetYoutubeLink(e.target.value)}
      />
      <button onClick={submitRequest}>Generate Quiz</button>
      //display the quiz
      {Quiz && (
        <div>
          <h2>Generated Quiz:</h2>
          <p>{Quiz}</p>
        </div>
      )}
    </div>
  );
};

export default Home;
