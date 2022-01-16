import platform, os, time, const
from db import DB
from inputhandler import InputHandler

class CLI:
    def __init__(self):
        self.DataBase = DB()
        self.DataBase.AddUser("CJ", "555-555-5555", "example@sample.com", "abc123")
        self.DataBase.PrintDebugTable()
        self.CurrentUserID = -1
        self.InputHandler = InputHandler()
        print(const.START_UP_TEXT)
        PlaySound(const.START_UP_SOUND_PATH)
        self.PublicMainMenu()
    
    def DrawMenu(self, Title, ListOfOptions):
        PrintHeader(Title)
        PossibleResponses = []
        for x in range(len(ListOfOptions)):
            PossibleResponses.append(x+1)
            print(f"{x+1}. {ListOfOptions[x]}")
        print()
        result = self.InputHandler.GetValidInput(AcceptableResponses=PossibleResponses)
        if result:
            return result
        return self.DrawMenu(Title, ListOfOptions)


    def PublicMainMenu(self):
        value = self.DrawMenu("Main Menu", ["Log In", "Create a New User", "Exit"])
        if value == 1:
            self.LogIn()
        elif value == 2:
            self.CreateNewUser()
        elif value == 3:
            self.Exit()
    
    def LoggedInMenu(self):
        Name = self.DataBase.FindUser(self.DataBase.SearchCriteria.ID, self.CurrentUserID)[1]
        value = self.DrawMenu(f"Welcome {Name}!", ["Change Email", "Change Name", "Change Phone Number", "Log Off", "Delete Account"])
        if value == 1:
            self.LogIn()
        elif value == 2:
            self.CreateNewUser()
        elif value == 3:
            self.Exit()
        elif value == 4:
            self.LogOff()
        elif value == 5:
            self.DeleteAccount()

    
    def LogOff(self):
        self.CurrentUserID = -1
        print(const.LOG_OFF_TEXT)
        PlaySound(const.LOG_OFF_SOUND_PATH)
        self.PublicMainMenu()
    
    def DeleteAccount(self):
        PrintHeader(const.DELETE_ACCOUNT_HEADER)
        answer = input(f"{const.DELETE_ACCOUNT_WARNING} Do you wish to continue? (Y/n) ").strip()
        if answer == "Y":
            Password = self.InputHandler.GetPassword(const.PASSWORD_PROMPT)
            if self.DataBase.DeleteUser(self.CurrentUserID, Password):
                Notice(const.DELETE_ACCOUNT_SUCCESS)
                self.LogOff()
            else:
                Notice(const.DELETE_ACCOUNT_FAIL)
                self.LoggedInMenu()
        else:
            self.LoggedInMenu()


    def CreateNewUser(self):
        PrintHeader(const.SIGN_UP_MENU_HEADER)
        print(const.SIGN_UP_DESC_TEXT)
        print()
        Name = self.InputHandler.GetValidInput(InputBehavior=self.InputHandler.InputBehavior.Raw, Message=const.SIGN_UP_NAME_PROMPT)
        print()
        Phone = self.InputHandler.GetValidInput(InputBehavior=self.InputHandler.InputBehavior.PhoneNumber, Message=const.SIGN_UP_PHONE_PROMPT, FailedMessage=const.SIGN_UP_PHONE_PROMPT_FAIL, RetryOnFail=True)
        print()
        Email = self.InputHandler.GetValidInput(InputBehavior=self.InputHandler.InputBehavior.Email, Message=const.EMAIL_PROMPT, FailedMessage=const.SIGN_UP_EMAIL_PROMPT_FAIL, RetryOnFail=True)
        print()
        while True:
            Password = self.InputHandler.GetPassword(const.SIGN_UP_PASSWORD_PROMPT)
            print()
            ConfirmPassword = self.InputHandler.GetPassword(const.SIGN_UP_PASSWORD_PROMPT_CONFIRM)
            print()
            if Password == ConfirmPassword:
                break
            else:
                Notice(const.SIGN_UP_PASSWORD_PROMPT_FAIL_TO_MATCH)
                print()
        self.DataBase.AddUser(Name, Phone, Email, Password)
        Notice(const.SIGN_UP_THANK_YOU)
        self.PublicMainMenu()
        
    def LogIn(self):
        PrintHeader(const.LOG_IN_HEADER)
        UserName = self.InputHandler.GetValidInput(InputBehavior=self.InputHandler.InputBehavior.Email, Message=const.EMAIL_PROMPT, FailedMessage=const.INVALID_EMAIL)
        print()
        if not UserName:
            self.LogIn()
        if not self.DataBase.DoesUserExist(UserName):
            Notice(const.NO_ACCOUNT_WITH_THIS_EMAIL)
            self.LogIn()
        Password = self.InputHandler.GetPassword(const.PASSWORD_PROMPT)
        self.CurrentUserID = self.DataBase.AttemptLogIn(UserName, Password)
        if self.CurrentUserID > 0:
            print()
            print(const.LOG_IN_TEXT)
            PlaySound(const.LOG_IN_SOUND_PATH)
            self.LoggedInMenu()
        else:
            Notice(const.INCORRECT_PASSWORD)
            self.LogIn()

    def Exit(self):
        print(const.SHUTDOWN_TEXT)
        PlaySound(const.SHUTDOWN_SOUND_PATH)
        quit()

def Notice(Message):
    print(Message)
    time.sleep(const.SLEEP_NOTICE)

def ClearScreen():
    if platform.system().lower()=="windows":
        os.system("cls")
    else:
        os.system("clear")

def PrintHeader(title):
    ClearScreen()
    print(f"{title}\n==========\n")

def PlaySound(URL):
    if platform.system().lower()=="windows":
        os.system(f"powershell -c (New-Object Media.SoundPlayer \"{URL}\").PlaySync();")
    # Sorry, only Windows users get the fun sound effects.
    