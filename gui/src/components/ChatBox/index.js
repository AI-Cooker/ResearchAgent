import classNames from 'classnames/bind';
import styles from './ChatBox.module.scss';
import { Input, Spin, Tooltip } from 'antd';
import { SendOutlined } from '@ant-design/icons';
import Message from '../Message';
import { useEffect, useRef, useState } from 'react';
import { useStore } from '~/store';
import { setCurrentSession, setMessageData } from '~/store/actions';

const { TextArea } = Input;
const cx = classNames.bind(styles);

const ChatBox = (props) => {
  const initSessionKey = () => {
    if (!sessionStorage.getItem('history')) {
      sessionStorage.setItem('history', JSON.stringify([]));
    }
    if (!sessionStorage.getItem('currentSessionId')) {
      sessionStorage.setItem('currentSessionId', '');
    }
  };
  initSessionKey();

  const maxToken = 2000;
  const [state, dispatch] = useStore();
  const [messageInput, setMessageInput] = useState('');
  const [limitToken, setLimitToken] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const bottomMessage = useRef(null);
  const { messageData, currentSessionId } = state;

  useEffect(() => {
    const storageId = sessionStorage.getItem('currentSessionId');
    dispatch(setCurrentSession(storageId));
    const storageMessageData = JSON.parse(sessionStorage.getItem(storageId));
    if (storageMessageData) {
      dispatch(setMessageData(storageMessageData));
    }
  }, []);

  useEffect(() => {
    if (currentSessionId) {
      sessionStorage.setItem(currentSessionId, JSON.stringify(messageData));
    }
    scrollToBottom();
  }, [messageData.length]);

  useEffect(() => {
    if (messageInput) {
      setLimitToken(messageInput.split(' ').length);
    } else {
      setLimitToken(0);
    }
  }, [messageInput]);

  const handleSendMessage = async (e) => {
    const currentMessageData = messageData;
    e.preventDefault();
    if (!messageInput) {
      return;
    }
    if (limitToken > maxToken) {
      return;
    }
    setMessageInput('');
    currentMessageData.push({
      position: 'right',
      message: `${messageInput}`,
      username: 'Username',
    });
    dispatch(setMessageData(currentMessageData));
    setIsLoading(true);
    await fetch('http://localhost:5690/ask_question', {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ user_input: messageInput }),
      credentials: 'include',
    })
      .then((res) => res.json())
      .then((data) => {
        currentMessageData.push({
          position: 'left',
          message: `${data['answer']}`,
          username: 'Bot',
        });
        dispatch(setMessageData(currentMessageData));
        setIsLoading(false);
      });
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
        {isLoading ? <Spin style={{ textAlign: 'left', padding: '10px' }}></Spin> : null}
        <div ref={bottomMessage}></div>
      </div>
      <span className={cx('Chatbox-token-limit')}>
        Limit Token: {limitToken}/{maxToken} Current Session: {currentSessionId}
      </span>
      <div className={cx('Chatbox-input-wrapper')}>
        <Tooltip title={currentSessionId ? null : 'Create new session first'}>
          <TextArea
            className={cx('Chatbox-textarea')}
            autoSize={{ minRows: 1, maxRows: 2 }}
            onChange={handleMessageInput}
            value={messageInput}
            placeholder="Enter your question..."
            disabled={!currentSessionId || isLoading ? true : false}
          />
        </Tooltip>
        {!currentSessionId || isLoading ? (
          <SendOutlined className={cx('Chatbox-send-button')} style={{ cursor: 'not-allowed' }} />
        ) : (
          <SendOutlined className={cx('Chatbox-send-button')} onClick={handleSendMessage} />
        )}
      </div>
    </div>
  );
};

export default ChatBox;
