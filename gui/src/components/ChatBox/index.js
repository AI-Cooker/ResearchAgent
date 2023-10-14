import classNames from 'classnames/bind';
import styles from './ChatBox.module.scss';
import { Input } from 'antd';
import { SendOutlined } from '@ant-design/icons';
import Message from '../Message';
import { useEffect, useRef, useState } from 'react';
import { json } from 'react-router-dom';

const { TextArea } = Input;
const cx = classNames.bind(styles);

const ChatBox = (props) => {
  const initSessionData = () => {
    const data = sessionStorage.getItem('data');
    if (!data) {
      sessionStorage.setItem('data', JSON.stringify([]));
    }
  };
  initSessionData();

  const [messageInput, setMessageInput] = useState('');
  const [messageData, setMessageData] = useState(JSON.parse(sessionStorage.getItem('data')));
  const bottomMessage = useRef(null);

  useEffect(() => {
    sessionStorage.setItem('data', JSON.stringify(messageData));
    scrollToBottom();
  }, [messageData.length]);

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (!messageInput) {
      return;
    }
    setMessageInput('');
    setMessageData(
      messageData.concat([
        {
          position: 'right',
          message: messageInput,
          username: 'Username',
        },
        {
          position: 'left',
          message: messageInput,
          username: 'Bot',
        },
      ]),
    );
  };

  const scrollToBottom = () => {
    bottomMessage.current.scrollIntoView({ behavior: 'smooth' });
  };

  const handleMessageInput = (e) => {
    setMessageInput(e.target.value);
  };

  return (
    <div className={cx('Chatbox-wrapper')}>
      <div className={cx('MessageBox-wrapper')}>
        {messageData.map((value, index) => {
          return <Message key={index} position={value.position} message={value.message} username={value.username} />;
        })}
        <div ref={bottomMessage}></div>
      </div>
      <div className={cx('Chatbox-input-wrapper')}>
        <TextArea
          className={cx('Chatbox-textarea')}
          autoSize={{ minRows: 1, maxRows: 2 }}
          onChange={handleMessageInput}
          value={messageInput}
          placeholder="Enter your question..."
        />
        <SendOutlined className={cx('Chatbox-send-button')} onClick={handleSendMessage} />
      </div>
    </div>
  );
};

export default ChatBox;