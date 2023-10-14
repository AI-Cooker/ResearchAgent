import { Layout } from 'antd';
import styles from './SideBar.module.scss';
import classNames from 'classnames/bind';
import { PlusOutlined } from '@ant-design/icons';
import { useStore } from '~/store';
import { actions } from '~/store';

const { Sider } = Layout;
const cx = classNames.bind(styles);

const SideBar = (props) => {
  const [state, dispatch] = useStore();
  return (
    <Sider className={cx('Sidebar-wrapper')}>
      <PlusOutlined
        onClick={() => {
          dispatch(actions.setMessageData([]));
        }}
      />
    </Sider>
  );
};

export default SideBar;
