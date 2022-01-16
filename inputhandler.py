import enum, const, time, re, getpass
from db import DB

class InputHandler:

    class InputBehavior(enum.Enum):
        Numeric = 0
        PhoneNumber = 1
        Email = 2
        ConvertToLower = 3
        Raw = 4
    
    def GetValidInput(self, MethodToRun = None, AcceptableResponses = None, InputBehavior = InputBehavior.Numeric, Message="Enter your Selection", FailedMessage="Invalid selection, please try again.", RetryOnFail=False):
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
            return self.GetValidInput(MethodToRun, AcceptableResponses, InputBehavior, Message, FailedMessage, RetryOnFail)
        else:
            return False
    
    def GetPassword(self, Message):
        return getpass.getpass(f"{Message}: ")
