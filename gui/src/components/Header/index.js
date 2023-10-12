import { Layout } from 'antd';

const { Header: HeaderAntd } = Layout;

const headerStyle = {
  textAlign: 'right',
  color: '#fff',
  height: 32,
  paddingInline: 25,
  lineHeight: '32px',
  backgroundColor: '#7dbcea',
};

const Header = (props) => {
  return <HeaderAntd style={headerStyle}>Header</HeaderAntd>;
};

export default Header;
