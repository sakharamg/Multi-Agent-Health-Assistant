"use client";
import React from "react";
import "regenerator-runtime/runtime";
import SpeechRecognition, {
  useSpeechRecognition,
} from "react-speech-recognition";

const Dictaphone = () => {
  const {
    transcript,
    listening,
    resetTranscript,
    browserSupportsSpeechRecognition,
  
  } = useSpeechRecognition();

  // if (!browserSupportsSpeechRecognition) {
  //   return <span>Browser doesn't support speech recognition.</span>;
  // }

  return (
    <div className="flex items-center">
      {/* <p>Microphone: {listening ? "on" : "off"}</p> */}
      {!listening && (
        <button
          className="bg-gradient-to-r from-blue-500 to-purple-700 w-12 h-12 text-white font-bold  pl-2 pr-2 py-2 rounded-full"
          onClick={SpeechRecognition.startListening}
        >
          <i className="fi fi-ss-microphone text-xl"></i>
        </button>
      )}
      {listening && (
        <button
          className="bg-red-600 w-12 h-12 text-white font-bold p-4 py-2 rounded-full"
          onClick={SpeechRecognition.stopListening}
        >
          <i className="fi fi-ss-microphone-slash text-xl"></i>
        </button>
      )}
      {/* <button onClick={resetTranscript}>Reset</button> */}
      {/* <p>{transcript}</p> */}
    </div>
  );
};
export default Dictaphone;
