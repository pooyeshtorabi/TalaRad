class StateManager:
    """
    A class for managing user states in the bot application.

    Attributes:
        user_states (dict): A dictionary mapping chat IDs to their state and associated data.
    """

    def __init__(self):
        """
        Initialize an empty state dictionary.
        """
        self.user_states = {}

    def set_state(self, chat_id, state, data=None):
        """
        Set the state and optional data for a given chat ID.

        :param chat_id: The unique identifier for the chat.
        :type chat_id: int
        :param state: The new state to set.
        :type state: str
        :param data: Optional dictionary containing additional data.
        :type data: dict, optional
        """
        self.user_states[chat_id] = {"state": state, "data": data if data else {}}

    def get_state(self, chat_id):
        """
        Retrieve the current state and data for a given chat ID.

        :param chat_id: The unique identifier for the chat.
        :type chat_id: int
        :return: A dictionary with the current state and data.
        :rtype: dict
        """
        return self.user_states.get(chat_id, {"state": "main", "data": {}})
