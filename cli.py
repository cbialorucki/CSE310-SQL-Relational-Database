import platform, os, time, const, datetime
from db import DB
from inputhandler import InputHandler

class CLI:
    """A command line application for interacting with a local database."""

    def __init__(self):
        self.Database = DB()
        self.CurrentUserID = -1
        self.InputHandler = InputHandler()
        
    def Launch(self):
        """Launches the program."""
        Notice(const.START_UP_TEXT)
        self.PublicMainMenu()
    
    def DrawMenu(self, Title, ListOfOptions, Details = None):
        """Draws a menu and returns the user's selection.

        :param Title str: The title of the menu to display.
        :param ListOfOptions list[str]: A list of options to display in the menu. Every option cooresponds to a possible return value.
        :param Details str: A description the appears below the header. (Default value = None)
        :returns: int: The number the user selected.

        """
        PrintHeader(Title)
        if Details:
            print(Details)
            print()
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
        """Launches and drives the main menu for users not logged in."""
        value = self.DrawMenu("Main Menu", ["Log In", "Create a New User", "View Statistical Information", "Exit"])
        if value == 1:
            self.LogIn()
        elif value == 2:
            self.CreateNewUser()
        elif value == 3:
            self.ShowStatisticalInformation()
        elif value == 4:
            self.Exit()
    
    def ShowStatisticalInformation(self):
        """Launches and drives the statistical information menu."""
        details = f"Total Users: {self.Database.GetTotalUsers()}\nSum of IDs: {self.Database.GetSumOfIDs()}\nMost Common Name: {self.Database.GetMostCommonName()}\nUptime: {str(self.Database.GetUptime())}"
        value = self.DrawMenu("View Statistical Information", ["Go Back"], details)
        if value == 1:
            self.PublicMainMenu()
    
    def LoggedInMenu(self):
        """Launches and drives the menu for logged in users."""
        Name = self.Database.FindUser(self.Database.UserAttribute.ID, self.CurrentUserID)[1]
        value = self.DrawMenu(f"Welcome {Name}!", ["Change Email", "Change Name", "Change Phone Number", "Change Password", "Log Off", "Delete Account"])
        if value == 1:
            self.DrawChangeValueMenu(self.Database.UserAttribute.Email)
        elif value == 2:
            self.DrawChangeValueMenu(self.Database.UserAttribute.Name)
        elif value == 3:
            self.DrawChangeValueMenu(self.Database.UserAttribute.Phone)
        elif value == 4:
            self.DrawChangeValueMenu(self.Database.UserAttribute.Password)
        elif value == 5:
            self.LogOff()
        elif value == 6:
            self.DeleteAccount()
    
    def DrawChangeValueMenu(self, UserAttribute):
        """Launches and drives a menu for changing an attribute of a logged in user account.

        :param UserAttribute DB.UserAttribute: The attribute to modify about a user account.

        """
        User = self.Database.FindUser(self.Database.UserAttribute.ID, self.CurrentUserID)
        Password = ""
        NewValue = ""
        if UserAttribute == self.Database.UserAttribute.Email:
            PrintHeader("Change Email")
            print(f"Your current email is {User[3]}")
            print()
            NewValue = self.InputHandler.GetValidInput(InputBehavior=self.InputHandler.InputBehavior.Email, Message="Enter your new email address", FailedMessage=const.INVALID_EMAIL, RetryOnFail=True)
        elif UserAttribute == self.Database.UserAttribute.Name:
            PrintHeader("Change Name")
            print(f"Your current name is {User[1]}")
            print()
            NewValue = input("Enter your new name: ").strip()
        elif UserAttribute == self.Database.UserAttribute.Phone:
            PrintHeader("Change Phone Number")
            OldPhoneNumber = f"({User[2][:3]}) {User[2][3:6]}-{User[2][6:]}"
            print(f"Your current phone number is {OldPhoneNumber}")
            print()
            NewValue = self.InputHandler.GetValidInput(InputBehavior=self.InputHandler.InputBehavior.PhoneNumber, Message="Enter your new phone number", FailedMessage=const.SIGN_UP_PHONE_PROMPT_FAIL, RetryOnFail=True)
        elif UserAttribute == self.Database.UserAttribute.Password:
            PrintHeader("Change Password")
            Password = self.InputHandler.GetPassword("Enter your old password")
            while True:
                NewValue = self.InputHandler.GetPassword("Enter your new password")
                ConfirmNewPassword = self.InputHandler.GetPassword("Confirm your new password")
                if NewValue == ConfirmNewPassword:
                    break
                else:
                    Notice(const.SIGN_UP_PASSWORD_PROMPT_FAIL_TO_MATCH)

        if Password == "":
            Password = self.InputHandler.GetPassword(const.PASSWORD_PROMPT)
        print()
        if self.Database.ChangeUserAttribute(self.CurrentUserID, UserAttribute, NewValue, Password):
            Notice("Successfully updated!")
        else:
            Notice("Update failed.")
        self.LoggedInMenu()

    def LogOff(self):
        """Logs off the current user account."""
        self.CurrentUserID = -1
        Notice(const.LOG_OFF_TEXT)
        self.PublicMainMenu()
    
    def DeleteAccount(self):
        """Launches and drives a menu for deleting the current user account."""
        PrintHeader(const.DELETE_ACCOUNT_HEADER)
        answer = input(f"{const.DELETE_ACCOUNT_WARNING} Do you wish to continue? (Y/n) ").strip()
        if answer == "Y":
            Password = self.InputHandler.GetPassword(const.PASSWORD_PROMPT)
            if self.Database.DeleteUser(self.CurrentUserID, Password):
                Notice(const.DELETE_ACCOUNT_SUCCESS)
                self.LogOff()
            else:
                Notice(const.DELETE_ACCOUNT_FAIL)
                self.LoggedInMenu()
        else:
            self.LoggedInMenu()

    def CreateNewUser(self):
        """Launches and drives a menu for creating a new user account."""
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
        self.Database.AddUser(Name, Phone, Email, Password)
        Notice(const.SIGN_UP_THANK_YOU)
        self.PublicMainMenu()
        
    def LogIn(self):
        """Launches and drives a menu to log into an existing user account."""
        PrintHeader(const.LOG_IN_HEADER)
        UserName = self.InputHandler.GetValidInput(InputBehavior=self.InputHandler.InputBehavior.Email, Message=const.EMAIL_PROMPT, FailedMessage=const.INVALID_EMAIL)
        print()
        if not UserName:
            self.LogIn()
        if not self.Database.DoesUserExist(UserName):
            Notice(const.NO_ACCOUNT_WITH_THIS_EMAIL)
            self.LogIn()
        Password = self.InputHandler.GetPassword(const.PASSWORD_PROMPT)
        self.CurrentUserID = self.Database.AttemptLogIn(UserName, Password)
        if self.CurrentUserID > 0:
            print()
            print(const.LOG_IN_TEXT)
            self.LoggedInMenu()
        else:
            Notice(const.INCORRECT_PASSWORD)
            self.LogIn()

    def Exit(self):
        """Closes the application."""
        Notice(const.SHUTDOWN_TEXT)
        quit()

def Notice(Message):
    """Displays a notice for a short amount of time before returning control to the user."""
    print(Message)
    time.sleep(const.SLEEP_NOTICE)

def ClearScreen():
    """Clears all text in the terminal window."""
    if platform.system().lower()=="windows":
        os.system("cls")
    else:
        os.system("clear")

def PrintHeader(title):
    """Clears the screen and prints a header for a menu."""
    ClearScreen()
    print(f"{title}\n==========\n")

    