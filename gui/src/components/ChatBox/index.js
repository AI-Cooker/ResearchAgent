import classNames from 'classnames/bind';
import styles from './ChatBox.module.scss';
import { Input } from 'antd';
import { SendOutlined } from '@ant-design/icons';

const { TextArea } = Input;
const cx = classNames.bind(styles);

const ChatBox = (props) => {
  return (
    <div className={cx('Chatbox-wrapper')}>
      <div className={cx('MessageBox-wrapper')}>
        <div style={{ textAlign: 'left', padding: '5px' }}>
          Aramco phải review xong Root cause analysis thì họ mới chịu upgrade cái mới, nên thứ 2 này chưa apply được, có
          thể phải sau đó trong tuần
        </div>
        <div style={{ textAlign: 'right', padding: '5px' }}>
          Aramco phải review xong Root cause analysis thì họ mới chịu upgrade cái mới, nên thứ 2 này chưa apply được, có
          thể phải sau đó trong tuần
        </div>
      </div>
      <div className={cx('Chatbox-input-wrapper')}>
        <TextArea className={cx('Chatbox-textarea')} autoSize={{ minRows: 1, maxRows: 2 }} />
        <SendOutlined className={cx('Chatbox-send-button')} />
      </div>
    </div>
  );
};

export default ChatBox;
