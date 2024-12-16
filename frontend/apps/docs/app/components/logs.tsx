import { MessageList, TypingIndicator, MessageSeparator, Message } from "@chatscope/chat-ui-kit-react";

const AgentLogs = ({chats}:{chats:[]})=>{
    return (
        <MessageList
          >
            {chats.map((m: { type: string; props: any }, i:number) =>
              m.type === "separator" ? (
                <MessageSeparator key={i} {...m.props} />
              ) : (
                <Message key={i} {...m.props} />
              )
            )}
          </MessageList>
    )
}

export default AgentLogs