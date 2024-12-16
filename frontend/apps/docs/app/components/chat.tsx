"use client";

import {
  MainContainer,
  ChatContainer,
  MessageList,
  Message,
  Sidebar,
  Avatar,
  Conversation,
  ConversationList,
  Search,
  ConversationHeader,
  MessageSeparator,
  TypingIndicator,
  ExpansionPanel,
  Button,
  MessageProps,
} from "@chatscope/chat-ui-kit-react";
import SmartWatch from "./smartwatch";
import IdCard from "./idcard";
import AgentLogs from "./logs";
import { HTMLAttributes, ReactNode, useEffect, useState } from "react";
import Summarizer from "./summarizer";
import Loading from "./loadingmodal";
import Reminders from "./reminders";
import { ENDPOINT } from "../consts/endpoint";

const ChatPage = ({
  chats,
  logs,
  status,
  trigger,
  setTrigger,
  setChats,
}: {
  chats: [
    {
      type: string;
      props: MessageProps &
        Omit<HTMLAttributes<HTMLElement>, "children" | keyof MessageProps> & {
          children?: ReactNode;
        };
      model: {
        message: string;
        sentTime: string;
        sender: string;
        direction: string;
        position: string;
      };
    },
  ];
  logs: [];
  status: string;
  setChats: (chat: any) => {};
}) => {
  const date = new Date();
  const [summarizerModal, setSummarizerModal] = useState(false);
  const [loading, setLoading] = useState(false);
  const [loadingtext, setLoadingText] = useState("");

  useEffect(()=>{
    if(trigger){
      handleSummarizerModal()
    }
  }, [trigger])

  const handleSummarizerModal = () => {
    setSummarizerModal(true);
  };
  const softSosChats = [
    {
      props: {
        model: {
          message: "<b><u>Simulator:</u></b>",
          sentTime: "15 mins ago",
          sender: "Elite",
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
            "Soft SOS triggered. Abnormal Vitals: {'oxygen': 89, 'heart_rate': 75, 'sleep': {'deep': 50, 'light': 333, 'rem': 131, 'awake': 49}}",
          sentTime: "15 mins ago",
          sender: "Elite",
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
          message: "<b><u>Planner:</u></b>",
          sentTime: "15 mins ago",
          sender: "Elite",
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
            "<b>REason: </b>Soft SoS has been triggered, so the system needs to notify the user about abnormal vitals",
          sentTime: "15 mins ago",
          sender: "Elite",
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
            "<b>ACTion: </b>Call notify_user to inform the user that the SOS process is being triggered.",
          sentTime: "15 mins ago",
          sender: "Elite",
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
          message: "<b><u>Caller Response:</u></b>",
          sentTime: "15 mins ago",
          sender: "Elite",
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
          message: "<b>Response: </b>Calling Notify Users API",
          sentTime: "15 mins ago",
          sender: "Elite",
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
          message: "<b>Tool: </b>notify_user",
          sentTime: "15 mins ago",
          sender: "Elite",
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
          message: `<b>Parameters: </b> {
                    "user_id": "DPFS304031",
                    "symptoms": "Soft SOS triggered. Abnormal vitals detected. \nIf you are feeling unwell, contact emergency services or book an appointment.}\n\nYour Vitals-\nHeart Rate: 75 (Normal range: 60-100 beats/min) bps \nOxygen: 89mm (Normal range: 75-100mm)\n<b><u>Deep Sleep: 50 minutes (Normal average: 70%) </u></b>\nLight Sleep: 333 minutes(Normal range: 25%)\nREM: 131 minutes (Normal range: 5%)\n<b><u>Awake: 49 minutes</u></b>`,
          sentTime: "15 mins ago",
          sender: "Elite",
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
          message: `<b>Inference: </b> \n Based on your weekly data, your sleep seems to have been little deviated from normal range.
          \nTo increase deep sleep percentage, you can:\n 
            Manage stress\n
            Eat mindfully\n
            Seek professional help if sleep problems are impacting your daily life\n
            Improve sleep hygiene by avoiding caffeine and alcohol close to bedtime, getting light exposure in the morning, and taking a warm shower or bath before bed`,
          sentTime: "15 mins ago",
          sender: "Elite",
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

  const handleSoftSos = () => {
    setLoading(true);
    setLoadingText("🪢 Fetching weekly records of User ID: 789");
    setTimeout(() => setLoadingText("⚙️ Analysing...."), 2000);
    setTimeout(
      () => setLoadingText("🚀 Sending report to LAM for inference..."),
      5000
    );
    setTimeout(() => setLoading(false), 7000);
    setTimeout(() => setSosChats(), 8000);
  };

  const handleHardSos = ()=>{
    setLoading(true);
    setLoadingText("🚨🚨🚨 Detected severe abnormality. Sending info to peers and ambulance...")
    setTimeout(()=>{
      fetch(`${ENDPOINT}/eliteapi/sendReminder/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ reminder: "!!!!Emergency!!!!\nYour friend Michael went unconscious at home.\nLocation: lat:15.6343435354 long:34.5343424235.\nPlease help the relevant authorities to reach him out immediately.\n~Sent from Samsung HardSoS service" }),
      })
    }, 5000)
    setTimeout(()=>setLoading(false), 5000)
  }

  const setSosChats = () => {
    setChats([]);
    var count = 0;
    const interval = setInterval(() => {
      setChats(softSosChats.slice(0, (count + 1) * 2));
      count++;
      if (count == 5) {
        clearInterval(interval);
      }
    }, 3000);
  };
  return (
    <div style={{ position: "relative", height: "90vh" }}>
      <Loading
        isLoading={loading}
        setLoading={setLoading}
        loaderText={loadingtext}
      />
      <MainContainer>
        <Sidebar position="left">
          <Search placeholder="Search..." />
          <ConversationList>
            <Conversation
              info="I am the executer"
              lastSenderName="xLam"
              name="xLam 3.5B"
              // className={status !== "" ? "bg-emerald-500" : ""}
            >
              <Avatar
                name="Lilly"
                src="https://chatscope.io/storybook/react/assets/lilly-aj6lnGPk.svg"
                status="available"
              />
            </Conversation>
            <Conversation
              info="I am Umi Planner"
              lastSenderName="Gyehoukja"
              name="Gyehoukja"
            >
              <Avatar
                name="Lilly"
                src="https://chatscope.io/storybook/react/assets/zoe-E7ZdmXF0.svg"
                status="available"
              />
            </Conversation>
            <Conversation
              info="I am RAG"
              lastSenderName="Smriti"
              name="Smriti"
              // className={status !== "" ? "rag-background" : ""}
            >
              <Avatar
                name="Lilly"
                src="https://chatscope.io/storybook/react/assets/eliot-JNkqSAth.svg"
                status="available"
              />
            </Conversation>
            <Conversation
              info="I am Qwen planner"
              lastSenderName="Qwen"
              name="Qwen 3B"
            >
              <Avatar
                name="Lilly"
                src="https://chatscope.io/storybook/react/assets/zoe-E7ZdmXF0.svg"
                status="unavailable"
              />
            </Conversation>
          </ConversationList>
          <IdCard
            name="Michael"
            id={789}
            gender={"Male"}
            age={22}
            icon={
              "https://media.licdn.com/dms/image/v2/D5603AQGFjuYg9H1BSg/profile-displayphoto-shrink_400_400/profile-displayphoto-shrink_400_400/0/1681481843764?e=2147483647&v=beta&t=r6B03hmRIA7q6KRkSd6jmotzlia7Q8lmT2-JwRUh_-U"
            }
          />
        </Sidebar>
        <Summarizer toggleModal={summarizerModal} setToggle={setSummarizerModal} />
        <ChatContainer>
          <ConversationHeader>
            <ConversationHeader.Back />
            <Avatar
              name="E.L.I.T.E"
              src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRHaZ9bsbOJ4y5Q-WSbxj2hnRMhLUDwCl3G9w&s"
            />
            <ConversationHeader.Content info="" userName="E.L.I.T.E" />
            <ConversationHeader.Actions></ConversationHeader.Actions>
          </ConversationHeader>
          <MessageList
            typingIndicator={
              status !== "" && <TypingIndicator content={status} />
            }
          >
            <MessageSeparator content={date.toUTCString()} />
            {chats.map((m, i) =>
              m.type === "separator" ? (
                <MessageSeparator key={i} {...m.props} />
              ) : (
                <Message key={i} {...m.props} />
              )
            )}
          </MessageList>
          {/* <MessageInput placeholder="Type message here" /> */}
        </ChatContainer>
        <Sidebar position="right">
          <ExpansionPanel open title="Smart Watch info">
            <SmartWatch />
          </ExpansionPanel>
          <ExpansionPanel title="Simulators">
            <Button
              border
              icon={
                <i className="fi fi-sr-light-emergency-on text-sm ml-2"></i>
              }
              labelPosition="left"
              onClick={() => {
                handleSoftSos();
              }}
            >
              Soft SoS simulator
            </Button>
            <br/>
            <Button
              border
              icon={<i className="fi fi-ss-triangle-warning text-sm ml-2"></i>}
              labelPosition="left"
              onClick={handleHardSos}
            >
              SoS simulator
            </Button>
            <Button
              border
              icon={<i className="fi fi-ss-triangle-warning text-sm ml-2"></i>}
              labelPosition="left"
              onClick={handleSummarizerModal}
            >
              Summarizer Simulator
            </Button>
          </ExpansionPanel>
          <ExpansionPanel title="Agent Logs">
            <AgentLogs chats={logs} />
          </ExpansionPanel>
          <ExpansionPanel title="Reminders">
            <Reminders />
          </ExpansionPanel>
        </Sidebar>
      </MainContainer>
    </div>
  );
};

export default ChatPage;
