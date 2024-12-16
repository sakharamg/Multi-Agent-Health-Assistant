"use client";
import React, { useEffect, useState } from "react";
import Dictaphone from "./components/mike";
import ChatPage from "./components/chat";
import { useSpeechRecognition } from "react-speech-recognition";
import { defChat } from "./consts/chats";
import { Avatar, TypingIndicator } from "@chatscope/chat-ui-kit-react";
import { ENDPOINT } from "./consts/endpoint";
import Loading from "./components/loadingmodal";
import Dropzone from "react-dropzone";
import FileUpload from "./components/fileupload";

export default function Page(): JSX.Element {
  const { transcript, listening } = useSpeechRecognition();
  const [input, setInput] = useState<string>();
  const [chats, setChats] = useState<any>(defChat);
  const [history, setHistory] = useState("");
  const [status, setStatus] = useState("");
  const [logs, setLogs] = useState<any>([]);
  const [triggerSummary, setTrigger] = useState(false)

  useEffect(() => {
    if (transcript) {
      setInput(transcript);
    }
  }, [listening]);

  

  const generateMessage = (message: string) => {
    setChats((chats: any) => [
      ...chats,
      {
        props: {
          model: {
            message: message,
            sentTime: "just now",
            sender: "elite",
            direction: "incoming",
            position: "single",
          },
        },
      },
    ]);
  };
  const sendMessage = (message: string | undefined) => {
    setChats((chats: any) => [
      ...chats,
      {
        props: {
          model: {
            message: message,
            sentTime: "just now",
            sender: "Sender",
            direction: "outgoing",
            position: "single",
          },
        },
      },
    ]);
  };

  const outputMessage = (res: { reason: string; action: string }) => {
    setLogs((logs: any) => [
      ...logs,
      {
        props: {
          model: {
            message:
              "<b className='text-emerald-500'><u>Planner Response</u></b>",
            sentTime: "just now",
            sender: "Sender",
            direction: "incoming",
            position: "single",
          },
          children: (
            <Avatar
              name="Elite"
              src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRHaZ9bsbOJ4y5Q-WSbxj2hnRMhLUDwCl3G9w&s"
              status="available"
            />
          ),
        },
      },
      {
        props: {
          model: {
            message: "<b>REason: </b> " + res.reason,
            sentTime: "just now",
            sender: "Sender",
            direction: "incoming",
            position: "single",
          },
          children: (
            <Avatar
              name="Elite"
              src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRHaZ9bsbOJ4y5Q-WSbxj2hnRMhLUDwCl3G9w&s"
              status="available"
            />
          ),
        },
      },
      {
        props: {
          model: {
            message: "<b>ACTion: </b> " + res.action,
            sentTime: "just now",
            sender: "Sender",
            direction: "incoming",
            position: "single",
          },
          children: (
            <Avatar
              name="Elite"
              src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRHaZ9bsbOJ4y5Q-WSbxj2hnRMhLUDwCl3G9w&s"
              status="available"
            />
          ),
        },
      },
    ]);
    setHistory(
      (history) =>
        history + "</s>Planner: " + JSON.stringify(res) + "</s>Action: "
    );
    console.log(history + "</s>Planner: " + JSON.stringify(res));
    return history + "</s>Planner: " + JSON.stringify(res) + "</s>Action: ";
  };
  const outputCallerMessage = (res: {
    [x: string]: string;
    tool: string;
    parameters: { questions: string; message: string };
  }) => {
    setLogs((logs: any) => [
      ...logs,
      {
        props: {
          model: {
            message:
              "<b className='text-emerald-500'><u>Caller Response</u></b>",
            sentTime: "just now",
            sender: "Sender",
            direction: "incoming",
            position: "single",
          },
          children: (
            <Avatar
              name="Elite"
              src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRHaZ9bsbOJ4y5Q-WSbxj2hnRMhLUDwCl3G9w&s"
              status="available"
            />
          ),
        },
      },
      {
        props: {
          model: {
            message: "<b>Tool: </b> " + res.tool,
            sentTime: "just now",
            sender: "Sender",
            direction: "incoming",
            position: "single",
          },
          children: (
            <Avatar
              name="Elite"
              src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRHaZ9bsbOJ4y5Q-WSbxj2hnRMhLUDwCl3G9w&s"
              status="available"
            />
          ),
        },
      },
      {
        props: {
          model: {
            message: "<b>Question: </b> " + res.parameters.questions,
            sentTime: "just now",
            sender: "Sender",
            direction: "incoming",
            position: "single",
          },
          children: (
            <Avatar
              name="Elite"
              src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRHaZ9bsbOJ4y5Q-WSbxj2hnRMhLUDwCl3G9w&s"
              status="available"
            />
          ),
        },
      },
      {
        props: {
          model: {
            message:
              "<b>Caller Parameters: </b> " + JSON.stringify(res.parameters),
            sentTime: "just now",
            sender: "Sender",
            direction: "incoming",
            position: "single",
          },
          children: (
            <Avatar
              name="Elite"
              src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRHaZ9bsbOJ4y5Q-WSbxj2hnRMhLUDwCl3G9w&s"
              status="available"
            />
          ),
        },
      },
    ]);
    setChats((chats: any) => {
      if (res.parameters.message != undefined) {
        return [
          ...chats,
          {
            props: {
              model: {
                message: "<b>Question: </b> " + res.parameters.questions,
                sentTime: "just now",
                sender: "Sender",
                direction: "incoming",
                position: "single",
              },
              children: (
                <Avatar
                  name="Elite"
                  src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRHaZ9bsbOJ4y5Q-WSbxj2hnRMhLUDwCl3G9w&s"
                  status="available"
                />
              ),
            },
          },
        ];
      }
      if (res.parameters.questions != undefined) {
        return [
          ...chats,
          {
            props: {
              model: {
                message: "<b>Question: </b> " + res.parameters.questions,
                sentTime: "just now",
                sender: "Sender",
                direction: "incoming",
                position: "single",
              },
              children: (
                <Avatar
                  name="Elite"
                  src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRHaZ9bsbOJ4y5Q-WSbxj2hnRMhLUDwCl3G9w&s"
                  status="available"
                />
              ),
            },
          },
        ];
      }
      return chats;
    });
    if ("history" in res) {
      console.log("in history");
      setHistory((history) => history + res["history"] + "Planner:");
      if(res.parameters.questions === undefined){
        getPlannerResponse(history + res["history"] + "Planner:")
      }
    } else {
      setHistory((history) => {
        const his = history + JSON.stringify(res);
        console.log(his);
        return his;
      });
    }
  };

  const handleKeyDown = (event: { key: string }) => {
    if (event.key === "Enter") {
      if (input !== "") {
        sendMessage(input);
      }
      setInput("");
      if (input == "give my weekly summary"){
        console.log("bruh here")
        setTrigger(true)
      }
      else if (input == "yes") {
        var result = confirm("Do you want to confirm the booking?");
        if (result) {
          alert("Booking successful!");
          generateMessage(
            "<b><u>Caller Response</u></b></br>Booked the slots successfully! and added it to user callendar with userid: 789"
          );
          setInput("");
        }
      } else {
        getPlannerResponse();
        setHistory((history) => history + "User:" + input);
        // setTimeout(()=>getPlannerResponse(), 500)
      }
    }
  };

  const getPlannerResponse = (q = undefined) => {
    var query;
    if (history != "") {
      query = history + "Observation: {'result':{'user': '" + input + "'}}";
    } else {
      query = "User: " + input;
    }
    if (input == "") {
      query = history;
    }
    if(q !== undefined){
      query = history+q;
    }
    const options = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query: query }),
    };
    setStatus("Planner is planning . . .");
    fetch(`${ENDPOINT}/eliteapi/plannerresp/`, options)
      .then((res) => res.json())
      .then((res) => {
        console.log(res);
        return outputMessage(res);
        // outputMessage("<b>Action: </b> "+ res.action)
      })
      .then((res) => {
        console.log("result: ", res);
        fetch(`${ENDPOINT}/eliteapi/callerresp/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ query: res }),
        })
          .then((res) => res.json())
          .then((res) => {
            outputCallerMessage(res);
            return res;
          })
          .then((res) => setStatus(""));
      })
      .then(() => setStatus("Caller is being called..."))
      .catch((e) => {
        alert("Some error occured!");
        setStatus("");
      });
  };

  return (
    <main className="bg-white h-[100vh]">
      <ChatPage chats={chats} status={status} setChats={setChats} logs={logs} trigger={triggerSummary} setTrigger={setTrigger}/>
      {/* {<TypingIndicator content={status}/>} */}
      <div className="flex items-center justify-center mx-4 my-2">
        <div className="w-3/5"/>
        <input
          className="appearance-none w-[90%] py-4 bg-blue-100 border-2 border-blue-300 rounded-full py-2 px-4 leading-tight focus:outline-none focus:bg-blue-200 focus:border-blue-500"
          type="text"
          value={input}
          onKeyDown={handleKeyDown}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Enter your health related query here..."
        />
        <button
          onClick={() => sendMessage(input)}
          className="bg-gradient-to-r from-emerald-400 to-emerald-600 mx-2 w-12 h-12 text-white font-bold p-4 py-2 rounded-full"
        >
          <i className="fi fi-sr-paper-plane-top"></i>
        </button>
        <Dictaphone />
        <FileUpload />
      </div>
    </main>
  );
}
