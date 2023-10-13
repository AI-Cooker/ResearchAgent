import { RightOutlined, LeftOutlined } from '@ant-design/icons';
import { Layout } from 'antd';
import SideBar from '../SideBar';
import ChatBox from '../ChatBox';
import { useState } from 'react';
import styles from './Content.module.scss';
import classNames from 'classnames/bind';

const { Content: ContentAntd } = Layout;
const cx = classNames.bind(styles);

const Content = (props) => {
  const [isShowSideBar, setIsShowSideBar] = useState(true);

  const handleShowSidebar = (e) => {
    e.preventDefault();
    setIsShowSideBar(!isShowSideBar);
  };

  return (
    <Layout hasSider className={cx("Content-wrapper")}>
      {isShowSideBar ? <SideBar /> : null}
      {isShowSideBar ? (
        <LeftOutlined style={{ cursor: 'pointer', backgroundColor: '#3ba0e9' }} onClick={handleShowSidebar} />
      ) : (
        <RightOutlined style={{ cursor: 'pointer', backgroundColor: '#3ba0e9' }} onClick={handleShowSidebar} />
      )}
      <ContentAntd>
        <ChatBox />
      </ContentAntd>
    </Layout>
  );
};

export default Content;
