import { constants } from '.';

const initState = {
  messageData: [],
  listSessionId: [],
  currentSessionId: '',
};

const Reducer = (state, action) => {
  switch (action.type) {
    case constants.SET_MESSAGE_DATA:
      return {
        ...state,
        messageData: action.payload,
      };
    case constants.SET_LIST_SESSION_ID:
      return {
        ...state,
        listSessionId: action.payload,
      };
    case constants.SET_CURRENT_SESSION:
      return {
        ...state,
        currentSessionId: action.payload,
      };
    default:
      throw new Error('Invalid action.');
  }
};

export { initState };
export default Reducer;
