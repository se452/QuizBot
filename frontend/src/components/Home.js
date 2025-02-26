import React, { useState } from "react";
import { CSSTransition, TransitionGroup } from "react-transition-group";
import "./Home.css";

const API_URL = process.env.NODE_ENV === 'production' 
  ? 'https://quiz-bot-iwzq.vercel.app'  // Your backend Vercel URL
  : 'http://localhost:5002';

const Home = () => {
  // State variables
  const [youtubeLink, setYoutubeLink] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [transcript, setTranscript] = useState("");
  const [quiz, setQuiz] = useState(null);
  const [userAnswers, setUserAnswers] = useState([]);
  const [quizSubmitted, setQuizSubmitted] = useState(false);
  const [quizResults, setQuizResults] = useState(null);

  // Function to generate quiz from YouTube link
  const generateQuiz = async () => {
    if (!youtubeLink) {
      setError("Please enter a YouTube link");
      return;
    }

    try {
      setIsLoading(true);
      setError("");
      setQuiz(null);
      setTranscript("");
      setQuizSubmitted(false);
      setQuizResults(null);

      const response = await fetch(`${API_URL}/api/generate-quiz`, {
        method: "POST",
        credentials: 'include',
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          youtube_url: youtubeLink,
          // You can add user_id here if you have authentication
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Failed to generate quiz");
      }

      setTranscript(data.transcript);
      setQuiz(data.quiz);
      // Initialize user answers array with -1 (no answer selected)
      setUserAnswers(new Array(data.quiz.questions.length).fill(-1));
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  // Function to handle answer selection
  const handleAnswerSelect = (questionIndex, answerIndex) => {
    console.log('Selected answer for question', questionIndex + 1, ':', answerIndex);
    const newAnswers = [...userAnswers];
    newAnswers[questionIndex] = answerIndex;
    setUserAnswers(newAnswers);
  };

  // Function to calculate results locally if backend fails
  const calculateResultsLocally = () => {
    const results = {
      score: 0,
      total: quiz.questions.length,
      question_results: [],
    };

    console.log('Starting local calculation...');
    
    quiz.questions.forEach((question, index) => {
      const userAnswer = userAnswers[index];
      const correctAnswer = question.correct_answers[0];  // Always use the first correct answer

      // Detailed debug logging
      console.log(`Question ${index + 1}:`);
      console.log('Question text:', question.question);
      console.log('User selected:', userAnswer, '(', question.options[userAnswer], ')');
      console.log('Correct answer:', correctAnswer, '(', question.options[correctAnswer], ')');
      console.log('All options:', question.options);
      
      const isCorrect = userAnswer === correctAnswer;
      console.log('Is correct?', isCorrect);
      
      if (isCorrect) {
        results.score++;
        console.log('Score increased to:', results.score);
      }

      results.question_results.push({
        question_index: index,
        is_correct: isCorrect,
        user_answer: userAnswer,
        correct_answer: correctAnswer,
        explanation: question.explanation,
        question_text: question.question,
        selected_option: question.options[userAnswer],
        correct_option: question.options[correctAnswer]
      });
    });

    results.percentage = (results.score / results.total) * 100;
    console.log('Final results:', results);
    return results;
  };

  // Function to submit quiz answers
  const submitQuiz = async () => {
    if (userAnswers.includes(-1)) {
      setError("Please answer all questions before submitting");
      return;
    }

    try {
      setIsLoading(true);
      setError("");

      console.log('Quiz submission - User answers:', userAnswers);
      console.log('Quiz submission - Questions:', quiz.questions.map((q, i) => ({
        question: q.question,
        userAnswer: userAnswers[i],
        userSelected: q.options[userAnswers[i]],
        correctAnswer: q.correct_answers[0],
        correctOption: q.options[q.correct_answers[0]]
      })));

      // Calculate results locally first
      const localResults = calculateResultsLocally();
      console.log('Local calculation results:', localResults);

      // Try to submit to backend
      try {
        const response = await fetch(`${API_URL}/api/submit-quiz`, {
          method: "POST",
          credentials: 'include',
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            quiz_id: quiz.id,
            answers: userAnswers,
            quiz_data: quiz
          }),
        });

        const data = await response.json();
        console.log('Backend response:', data);

        if (!response.ok) {
          throw new Error(data.error || "Failed to submit quiz");
        }

        // Compare backend results with local results
        console.log('Backend vs Local results:');
        console.log('Backend score:', data.results.score);
        console.log('Local score:', localResults.score);
        
        // Use local results if they differ significantly
        if (Math.abs(data.results.score - localResults.score) > 2) {
          console.warn('Significant difference between backend and local results. Using local results.');
          setQuizResults(localResults);
        } else {
          setQuizResults(data.results);
        }
        
        setQuizSubmitted(true);
      } catch (backendError) {
        console.error("Backend submission failed, using local results:", backendError);
        setQuizResults(localResults);
        setQuizSubmitted(true);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  // Function to reset the quiz
  const resetQuiz = () => {
    setYoutubeLink("");
    setQuiz(null);
    setTranscript("");
    setUserAnswers([]);
    setQuizSubmitted(false);
    setQuizResults(null);
    setError("");
  };

  return (
    <div className="home-styling">
      {/* Hero Section */}
      <div className="hero-section">
        <h1>QuizBot</h1>
        <p>Transform any YouTube video into an interactive quiz in seconds. Perfect for learning, teaching, or just having fun!</p>
      </div>

      {/* Input Section */}
      <div className="input-section">
        <input
          type="text"
          placeholder="Paste your YouTube video URL here..."
          value={youtubeLink}
          onChange={(e) => setYoutubeLink(e.target.value)}
          disabled={isLoading}
        />
        <button onClick={generateQuiz} disabled={isLoading}>
          {isLoading ? "Generating..." : "Generate Quiz"}
        </button>
      </div>

      {/* Error Message */}
      {error && <div className="error-message">{error}</div>}

      {/* Loading Spinner */}
      {isLoading && <div className="loading-spinner" />}

      {/* Transcript Section */}
      {transcript && (
        <div className="transcript-section">
          <h2>Video Transcript</h2>
          <div className="transcript-content">{transcript}</div>
        </div>
      )}

      {/* Quiz Section */}
      {quiz && !quizSubmitted && (
        <div className="quiz-section">
          <h2>Quiz Time!</h2>
          <div>
            {quiz.questions.map((question, qIndex) => (
              <div key={qIndex} className="question-card">
                <h3>Question {qIndex + 1}</h3>
                <p>{question.question}</p>
                <div className="options">
                  {question.options.map((option, oIndex) => (
                    <div
                      key={oIndex}
                      className={`option ${
                        userAnswers[qIndex] === oIndex ? "selected" : ""
                      }`}
                    >
                      <input
                        type="radio"
                        id={`q${qIndex}-o${oIndex}`}
                        name={`question-${qIndex}`}
                        checked={userAnswers[qIndex] === oIndex}
                        onChange={() => handleAnswerSelect(qIndex, oIndex)}
                      />
                      <label htmlFor={`q${qIndex}-o${oIndex}`}>{option}</label>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
          <button
            onClick={submitQuiz}
            disabled={userAnswers.includes(-1)}
            className="submit-button"
          >
            Submit Quiz
          </button>
        </div>
      )}

      {/* Results Section */}
      {quizSubmitted && quizResults && (
        <div className="results-section">
          <div className="score-card">
            <h3>Your Score: {quizResults.score}/{quizResults.total}</h3>
            <p>{quizResults.percentage.toFixed(2)}%</p>
          </div>

          <div>
            {quizResults.question_results.map((result, index) => (
              <div
                key={index}
                className={`result-card ${
                  result.is_correct ? "correct" : "incorrect"
                }`}
              >
                <div
                  className={`result-status ${
                    result.is_correct ? "correct" : "incorrect"
                  }`}
                >
                  {result.is_correct ? "Correct ✓" : "Incorrect ✗"}
                </div>
                <h3>Question {index + 1}</h3>
                <p>{quiz.questions[index].question}</p>

                <div className="options-result">
                  {quiz.questions[index].options.map((option, oIndex) => (
                    <div
                      key={oIndex}
                      className={`
                        option-result
                        ${oIndex === result.user_answer ? "user-selected" : ""}
                        ${
                          oIndex === result.correct_answer ? "correct-answer" : ""
                        }
                      `}
                    >
                      {option}
                      {oIndex === result.correct_answer && (
                        <span className="correct-label"> (Correct Answer)</span>
                      )}
                    </div>
                  ))}
                </div>

                <div className="explanation">
                  <strong>Explanation:</strong>
                  <p>{result.explanation || quiz.questions[index].explanation}</p>
                </div>
              </div>
            ))}
          </div>

          <button onClick={resetQuiz} className="reset-button">
            Try Another Video
          </button>
        </div>
      )}
    </div>
  );
};

export default Home;
