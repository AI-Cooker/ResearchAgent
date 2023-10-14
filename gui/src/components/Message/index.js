import { Fragment } from 'react';
import styles from './Message.module.scss';
import classNames from 'classnames/bind';
import Markdown from 'react-markdown';

const cx = classNames.bind(styles);

const Message = (props) => {
  return (
      <div className={props.position === 'right' ? cx('Message-user-wrapper') : cx('Message-bot-wrapper')}>
        <div className={props.position === 'right' ? cx('Message-user') : cx('Message-bot')}>
          <Markdown>{props.message}</Markdown>
        </div>
      </div>
  );
};

export default Message;
