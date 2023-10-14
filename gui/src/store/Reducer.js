import { constants } from '.';

const initState = {
  messageData: [],
};

const Reducer = (state, action) => {
  switch (action.type) {
    case constants.SET_MESSAGE_DATA:
      return {
        ...state,
        messageData: action.payload,
      };
    default:
      throw new Error("Invalid action.")
  }
};

export { initState };
export default Reducer;
