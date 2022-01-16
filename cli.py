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
        print("Welcome to Example Corporation's Database!")
        PlaySound("https://www.winhistory.de/more/winstart/down/o98.wav")
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
        value = self.DrawMenu(f"Welcome {Name}!", ["Change Email", "Change Name", "Change Phone Number", "Log Out", "Delete Account"])
        if value == 1:
            self.LogIn()
        elif value == 2:
            self.CreateNewUser()
        elif value == 3:
            self.Exit()
        elif value == 4:
            self.LogOff()
    
    def LogOff(self):
        self.CurrentUserID = -1
        print("You have been logged off.")
        PlaySound("https://www.winhistory.de/more/winstart/down/winxpshutdown.wav")
        self.PublicMainMenu()

    def CreateNewUser(self):
        PrintHeader("Create a New User")
        print("To create a new user, we need your name, phone number, email address, and a new password.\n\n")
        Name = self.InputHandler.GetValidInput(InputBehavior=self.InputHandler.InputBehavior.Raw, Message="Enter your Name")
        print()
        Phone = self.InputHandler.GetValidInput(InputBehavior=self.InputHandler.InputBehavior.PhoneNumber, Message="Enter your Phone Number", FailedMessage="You entered an invalid phone number. Please provide a valid, 10 digit US phone number.", RetryOnFail=True)
        print()
        Email = self.InputHandler.GetValidInput(InputBehavior=self.InputHandler.InputBehavior.Email, Message="Enter your Email Address", FailedMessage="You entered an invalid email address. Please provide a valid email address", RetryOnFail=True)
        print()
        while True:
            Password = self.InputHandler.GetPassword("Enter your Password")
            print()
            ConfirmPassword = self.InputHandler.GetPassword("Confirm your Password")
            print()
            if Password == ConfirmPassword:
                break
            else:
                Notice("Your passwords did not match. Please try again.")
                print()
        self.DataBase.AddUser(Name, Phone, Email, Password)
        Notice("Thank you for creating your account!")
        self.PublicMainMenu()
        
    def LogIn(self):
        PrintHeader("Log In")
        UserName = input("Enter your Email Address or Phone Number: ")
        print()
        if not self.DataBase.DoesUserExist(UserName):
            Notice("Invalid username. Please try again.")
            self.LogIn()
        Password = input("Enter your Password: ")
        self.CurrentUserID = self.DataBase.AttemptLogIn(UserName, Password)
        if self.CurrentUserID > 0:
            print()
            print("Log In Success!")
            PlaySound("https://www.winhistory.de/more/winstart/down/oxp.wav")
            self.LoggedInMenu()
        else:
            Notice("Incorrect password. Please try again.")
            self.LogIn()

    def Exit(self):
        print("Shutting down...")
        PlaySound("https://www.winhistory.de/more/winstart/down/win98logoff.wav")
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
        #pass
    # Sorry, only Windows users get the fun sound effects.
    