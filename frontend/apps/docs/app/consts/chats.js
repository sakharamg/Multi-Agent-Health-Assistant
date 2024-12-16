import { Avatar } from "@chatscope/chat-ui-kit-react";
export const defChat = [
  {
    props: {
      model: {
        message: "Hi I Elite, a health care bot",
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
        message: "How can I assist you?",
        sentTime: "15 mins ago",
        sender: "Elite",
        direction: "incoming",
        position: "single",
      },
      children: (
        <Avatar
          name="Lilly"
          src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRHaZ9bsbOJ4y5Q-WSbxj2hnRMhLUDwCl3G9w&s"
          status="available"
        />
      ),
    },
  },
];
