import enum, const, time, re, getpass
from db import DB

class InputHandler:

    """A class to handle data input."""

    class InputBehavior(enum.Enum):
        """An enum to describe different available input behaviors."""
        Numeric = 0
        PhoneNumber = 1
        Email = 2
        ConvertToLower = 3
        Raw = 4
    
    def GetValidInput(self, AcceptableResponses = None, InputBehavior = InputBehavior.Numeric, Message="Enter your Selection", FailedMessage="Invalid selection, please try again.", RetryOnFail=False):
        """Gets a valid input for a set of conditions.

        :param AcceptableResponses list[str]: A list of acceptable responses. If no list is provided, the function will not validate against this list. (Default value = None)
        :param InputBehavior InputBehavior: Limits what type of input is allowed. (Default value = InputBehavior.Numeric)
        :param Message str: The message to display when asking for input. (Default value = "Enter your Selection")
        :param FailedMessage str: The message to display when the input is invalid. (Default value = "Invalid selection, please try again.")
        :param RetryOnFail bool: If True, will try to get input from the user again if the input is invalid. If False, the function will return False if the user fails to enter valid data. (Default value = False)
        :returns: str: The valid input from the user, or False if the user gives invalid data and RetryOnFail is False.

        """
        value = input(f"{Message}: ").strip()
        if InputBehavior == self.InputBehavior.Numeric:
            if value.isnumeric():
                if AcceptableResponses == None or int(value) in AcceptableResponses:
                    return int(value)
        elif InputBehavior == self.InputBehavior.PhoneNumber:
            PhoneNumber = DB.IsPhoneValid(value)
            if PhoneNumber:
                return PhoneNumber
        elif InputBehavior == self.InputBehavior.Email:
            Email = DB.IsEmailValid(value)
            if Email:
                return Email
        elif InputBehavior == self.InputBehavior.ConvertToLower:
            if AcceptableResponses == None or value.lower() in AcceptableResponses:
                return value.lower()
        elif InputBehavior == self.InputBehavior.Raw:
            if AcceptableResponses == None or value in AcceptableResponses:
                return value

        print()
        print(FailedMessage)
        print()
        time.sleep(const.SLEEP_NOTICE)

        if RetryOnFail:
            return self.GetValidInput(AcceptableResponses, InputBehavior, Message, FailedMessage, RetryOnFail)
        else:
            return False
    
    def GetPassword(self, Message = "Password"):
        """Gets a password input without echoing characters to the terminal window.

        :param Message str: The message to display when asking the user for their password. (Default value = Password)

        :returns: str: The password entered by the user.

        """
        return getpass.getpass(f"{Message}: ")
