import { Layout } from 'antd';
import Header from '../Header';
import Footer from '../Footer';
import Content from '../Content';
import styles from './Home.module.scss';
import classNames from 'classnames/bind';

const cx = classNames.bind(styles);

const Home = (props) => {
  return (
    <Layout className={cx('Home-wrapper')}>
      <Header />
      <Content />
      <Footer />
    </Layout>
  );
};

export default Home;
