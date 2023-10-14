import { Fragment } from 'react';
import styles from './Message.module.scss';
import classNames from 'classnames/bind';

const cx = classNames.bind(styles);

const Message = (props) => {
  return (
    <Fragment>
      {/* <Divider
        orientation={props.position}
        orientationMargin="0px"
        plain
        className={props.position === 'right' ? cx('Message-divider-user') : cx('Message-divider-bot')}
      >
        <p className={props.position === 'right' ? cx('Message-name-user') : cx('Message-name-bot')}>
          {props.username}
        </p>
      </Divider> */}
      <div className={props.position === 'right' ? cx('Message-user-wrapper') : cx('Message-bot-wrapper')}>
        <p className={props.position === 'right' ? cx('Message-user') : cx('Message-bot')}>{props.message}</p>
      </div>
    </Fragment>
  );
};

export default Message;
