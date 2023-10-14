import { SET_MESSAGE_DATA, GET_MESSAGE_DATA } from './constants';

export const setMessageData = (payload) => ({
  type: SET_MESSAGE_DATA,
  payload: payload,
});
