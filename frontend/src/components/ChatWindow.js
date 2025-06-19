import React from 'react';
import Message from './Message';
import useScrollToBottom from '../hooks/useScrollToBottom';
import LoadingProgress from './LoadingProgress';
import '../styles/chat-window.css';

const ChatWindow = ({ messages, isTyping }) => {
  const messagesEndRef = useScrollToBottom(messages, isTyping);

  return (
    <div className="flex-1 p-2 sm:p-6 flex flex-col overflow-hidden bg-gray-50 rounded-lg">
      <div className="flex-1 overflow-y-auto w-full">
        <div className="space-y-2 px-2 sm:px-8 pb-20">
          {messages.map((msg, index) => (
            <Message key={index} message={msg} />
          ))}
          {isTyping && (
            <div className="flex items-center space-x-2">
              <div className="flex-shrink-0 h-10 w-10 rounded-full bg-gradient-to-r from-blue-500 to-blue-600 flex items-center justify-center text-white text-lg">
                📊
              </div>
              <LoadingProgress />
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>
    </div>
  );
};

export default ChatWindow;