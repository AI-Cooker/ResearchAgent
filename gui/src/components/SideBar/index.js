import { Layout } from 'antd';

const { Sider } = Layout;

const siderStyle = {
  textAlign: 'center',
  lineHeight: '120px',
  color: '#fff',
  backgroundColor: '#3ba0e9',
};

const SideBar = (props) => {
  return <Sider style={siderStyle}>Sidebar</Sider>;
};

export default SideBar;
