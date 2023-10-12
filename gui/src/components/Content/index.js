import { RightOutlined, LeftOutlined } from '@ant-design/icons';
import { Layout } from 'antd';
import SideBar from '../SideBar';
import { useState } from 'react';

const { Content: ContentAntd } = Layout;
const contentStyle = {
  textAlign: 'center',
  minHeight: 120,
  lineHeight: '120px',
  color: '#fff',
  backgroundColor: '#108ee9',
};

const Content = (props) => {
  const [isShowSideBar, setIsShowSideBar] = useState(true);

  const handleShowSidebar = (e) => {
    e.preventDefault();
    setIsShowSideBar(!isShowSideBar);
  };

  return (
    <Layout hasSider>
      {isShowSideBar ? <SideBar /> : null}
      {isShowSideBar ? (
        <LeftOutlined style={{ cursor: 'pointer', backgroundColor: '#3ba0e9' }} onClick={handleShowSidebar} />
      ) : (
        <RightOutlined style={{ cursor: 'pointer', backgroundColor: '#3ba0e9' }} onClick={handleShowSidebar} />
      )}
      <ContentAntd style={contentStyle}>Content</ContentAntd>
    </Layout>
  );
};

export default Content;
