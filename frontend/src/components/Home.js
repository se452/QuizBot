import Homepage from "./routes/home.js"; //importing homepage
import React , {useState} from "react";
import axios from "axios";

const Home = () => {

//state constants can be edited
    const[YoutubeLink , SetYoutubeLink] = useState(""); //to store link
    const[Transcript , SetTranscript] = useState(""); // to store transcript
    const[Quiz , SetQuiz] = useState("");//to store quiz


    const submitRequest = () =>{
      //handle api requests
    }

    return(

        <div>
            <h1>Quiz Generator</h1>
            <input
                type = "text"
                placeholder = "Enter the Link"
                value = {youtubeLink}
                onChange = {(e) => SetYoutubeLink(e.target.value)}
            />

            <button onClick = {submitRequest}>Generate Quiz</button>

            //display the quiz
            {quiz && (
                 <div>
                     <h2>Generated Quiz:</h2>
                     <p>{quiz}</p>
                 </div>
                    )}

        </div>


    );


export default Home;
