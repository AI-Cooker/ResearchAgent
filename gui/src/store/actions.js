import { SET_MESSAGE_DATA, SET_LIST_SESSION_ID, SET_CURRENT_SESSION } from './constants';

export const setMessageData = (payload) => ({
  type: SET_MESSAGE_DATA,
  payload: payload,
});

export const setListSessionId = (payload) => ({
  type: SET_LIST_SESSION_ID,
  payload: payload,
});

export const setCurrentSession = (payload) => ({
  type: SET_CURRENT_SESSION,
  payload: payload,
});
