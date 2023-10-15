import { Layout, Button, Divider } from 'antd';
import styles from './SideBar.module.scss';
import classNames from 'classnames/bind';
import { PlusOutlined } from '@ant-design/icons';
import { useStore } from '~/store';
import { actions } from '~/store';
import { useEffect, useState } from 'react';

const { Sider } = Layout;
const cx = classNames.bind(styles);

const SideBar = (props) => {
  const [state, dispatch] = useStore();
  const { listSessionId, currentSessionId } = state;

  const handleNewSession = async (e) => {
    e.preventDefault();
    dispatch(actions.setMessageData([]));
    await fetch('http://127.0.0.1:5690/new_chat', { method: 'POST', credentials: 'include' })
      .then((res) => res.json())
      .then((data) => {
        const sessionId = data['session_id'];
        dispatch(actions.setCurrentSession(sessionId));
        if (currentSessionId) {
          dispatch(actions.setListSessionId(listSessionId.concat([currentSessionId])));
        }
      });
  };

  return (
    <Sider className={cx('Sidebar-wrapper')}>
      <Button className={cx('Sidebar-button')} icon={<PlusOutlined />} onClick={handleNewSession}>
        New Session
      </Button>
      <Divider className={cx('Sidebar-divider')}></Divider>
      {listSessionId.map((value, index) => {
        return (
          <Button key={index} className={cx('Sidebar-button')}>
            {value.slice(0, 6)}
          </Button>
        );
      })}
    </Sider>
  );
};

export default SideBar;
