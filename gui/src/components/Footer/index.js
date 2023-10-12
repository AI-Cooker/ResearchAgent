import { Layout } from 'antd';

const { Footer: FooterAntd } = Layout;
const footerStyle = {
  textAlign: 'center',
  color: '#fff',
  backgroundColor: '#7dbcea',
};

const Footer = (props) => {
  return <FooterAntd style={footerStyle}>Footer</FooterAntd>;
};

export default Footer;
