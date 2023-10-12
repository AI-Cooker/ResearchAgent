import { Layout } from 'antd';
import Header from '../Header';
import Footer from '../Footer';
import Content from '../Content';

const Home = (props) => {
  return (
    <Layout>
      <Header />
      <Content />
      <Footer />
    </Layout>
  );
};

export default Home;
