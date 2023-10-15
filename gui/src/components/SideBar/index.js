import { Layout, Button, Divider, Modal } from 'antd';
import styles from './SideBar.module.scss';
import classNames from 'classnames/bind';
import { PlusOutlined } from '@ant-design/icons';
import { useStore } from '~/store';
import { actions } from '~/store';
import { useEffect, useState } from 'react';
import Message from '../Message';

const { Sider } = Layout;
const cx = classNames.bind(styles);

const SideBar = (props) => {
  const [state, dispatch] = useStore();
  const { listSessionId, currentSessionId } = state;
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [modelMessageData, setModelMessageData] = useState([]);
  const [modelSessionId, setModelSessionId] = useState('');

  const showModal = (value) => {
    const sessionId = value;
    setModelSessionId(sessionId);
    const data = JSON.parse(sessionStorage.getItem(sessionId));
    if (data) {
      setModelMessageData(data);
    }
    setIsModalOpen(true);
  };

  const handleOk = () => {
    setIsModalOpen(false);
  };

  const handleCancel = () => {
    setIsModalOpen(false);
  };

  useEffect(() => {
    const storageHistory = JSON.parse(sessionStorage.getItem('history'));
    if (!storageHistory) {
      return;
    }
    dispatch(actions.setListSessionId(storageHistory));
  }, []);

  const pushSessionToHistory = () => {
    if (!currentSessionId) {
      return;
    }
    const storageHistory = JSON.parse(sessionStorage.getItem('history'));
    storageHistory.push(currentSessionId);
    sessionStorage.setItem('history', JSON.stringify(storageHistory));
    dispatch(actions.setListSessionId(storageHistory));
  };

  const handleNewSession = async (e) => {
    e.preventDefault();
    //Push session history must run before fetch API
    pushSessionToHistory();
    await fetch('http://localhost:5690/new_chat', { method: 'POST', credentials: 'include' })
      .then((res) => res.json())
      .then((data) => {
        const sessionId = data['session_id'];
        dispatch(actions.setCurrentSession(sessionId));
        dispatch(actions.setMessageData([]));
        sessionStorage.setItem('currentSessionId', sessionId);
        sessionStorage.setItem(sessionId, JSON.stringify([]));
      });
  };

  return (
    <Sider className={cx('Sidebar-wrapper')}>
      <Button className={cx('Sidebar-button')} icon={<PlusOutlined />} onClick={handleNewSession}>
        New Session
      </Button>
      <Divider className={cx('Sidebar-divider')}></Divider>
      {listSessionId.map((data, index) => {
        return (
          <Button
            key={index}
            className={cx('Sidebar-button')}
            onClick={() => {
              showModal(data);
            }}
            value={data}
          >
            {data.slice(0, 6)}
          </Button>
        );
      })}
      <Modal title={modelSessionId} open={isModalOpen} onOk={handleOk} onCancel={handleCancel} width={1000}>
        <div className={cx('Sidebar-modal')}>
          {modelMessageData.map((data, index) => {
            return (
              <Message key={index} position={data.position} message={data.message} username={data.username}></Message>
            );
          })}
        </div>
      </Modal>
    </Sider>
  );
};

export default SideBar;
