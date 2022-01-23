from fileinput import filename
from datetime import datetime
import sqlite3, enum, re, const

class DB:
    """A local database to demonstrate a login system."""
    
    class UserAttribute(enum.Enum):
        """An enum used to describe different acceptable user attributes."""
        ID = 0
        Name = 1
        Phone = 2
        Email = 3
        Password = 4

    def __init__(self, FilePath = const.RAM_DB_PATH):
        self._db = sqlite3.connect(FilePath)

        self._db.cursor().execute('''CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT, phone TEXT unique, email TEXT unique, password TEXT)''')
        self._db.commit()

        self.StartedTime = datetime.now()

    def AddUser(self, Name, Phone, Email, Password):
        """Adds a user account to the current database.

        :param Name str: The name of the new user.
        :param Phone str: The phone number of the new user.
        :param Email str: The email address of the new user.
        :param Password str: The password the new user selected for their account.
        :returns: bool: True if the account creation was successful, False if it was unsuccessful.

        """
        Email = Email.lower()
        if self.FindUser(self.UserAttribute.Phone, Phone) or self.FindUser(self.UserAttribute.Email, Email):
            return False
        self._db.cursor().execute('''INSERT INTO users(name, phone, email, password) VALUES(?,?,?,?)''', (Name, Phone, Email, Password))
        self._db.commit()
        return True
    
    def PrintDebugTable(self):
        """Prints a table to the terminal window for debugging purposes."""
        print(self._db.cursor().execute('''SELECT * FROM users''').fetchall())

    def FindUser(self, UserAttribute, Input):
        """Finds a user account for a given input.

        :param UserAttribute DB.UserAttribute: The user attribute to use for searching for the user.
        :param Input str: The string used to search for the user according to the UserAttribute.
        :returns: list[str]: A list containing the ID, Name, Phone, and Email Address of the found user.

        """
        if UserAttribute == self.UserAttribute.Name:
            return self._db.cursor().execute('''SELECT id, name, phone, email FROM users WHERE name=?''', (Input,)).fetchall()
        elif UserAttribute == self.UserAttribute.Phone:
            return self._db.cursor().execute('''SELECT id, name, phone, email FROM users WHERE phone=?''', (Input,)).fetchone()
        elif UserAttribute == self.UserAttribute.Email:
            return self._db.cursor().execute('''SELECT id, name, phone, email FROM users WHERE email=?''', (Input,)).fetchone()
        elif UserAttribute == self.UserAttribute.ID:
            return self._db.cursor().execute('''SELECT id, name, phone, email FROM users WHERE id=?''', (Input,)).fetchone()
        return False

    def DoesUserExist(self, Email):
        """Finds if a user account exists.

        :param Email str: The email address for the user account.
        :returns: bool: True if the user account exists in the database, False if the user account does not.

        """
        if self.FindUser(self.UserAttribute.Email, Email):
            return True
        return False

    def AttemptLogIn(self, Email, Password):
        """Attempts to log in the user.

        :param Email str: The email address for the user account.
        :param Password str: The password used to try logging in.
        :returns: int: The user account ID if the log in was successful, False if the user account does not.

        """
        User = self.FindUser(self.UserAttribute.Email, Email)
        if User:
            if self._DoesPasswordMatch(User[0], Password):
                return User[0]
        return False
    
    def _DoesPasswordMatch(self, UserID, Password):
        """Notifies if a password matches for a specified user.

        :param UserID int: The ID of the user account to test if the password matches.
        :param Password str: The password used to try matching it.
        :returns: bool: True if the password was correct, False if the password was not.

        """
        CorrectPassword = self._db.cursor().execute('''SELECT password FROM users WHERE id=?''', (UserID,)).fetchall()[0][0]
        return Password == CorrectPassword

    def DeleteUser(self, UserID, Password):
        """Deletes a specified user.

        :param UserID int: The ID of the user account to delete.
        :param Password str: The password used for the user account.
        :returns: bool: True if the account deletion was successful, False if it was not.

        """
        if self._DoesPasswordMatch(UserID, Password):
            self._db.cursor().execute('''DELETE FROM users WHERE id=? ''', (UserID,))
            self._db.commit()
            return True
        return False
    
    def ChangeUserAttribute(self, UserID, UserAttribute, Value, Password):
        """Changes an attribute about a user.

        :param UserID int: The ID for the user account.
        :param UserAttribute DB.UserAttribute: The attribute to change about the user account.
        :param Value str: The new value for the specified attribute.
        :param Password str: The password used for the user account.
        :returns: bool: True if the change was successful, False if the user account does not.

        """
        Value = Value.strip()
        if self._DoesPasswordMatch(UserID, Password):
            if UserAttribute == self.UserAttribute.Email and self.IsEmailValid(Value):
                self._db.cursor().execute('''UPDATE users SET email=? WHERE id=? ''', (self.IsEmailValid(Value),UserID))
            elif UserAttribute == self.UserAttribute.Name:
                self._db.cursor().execute('''UPDATE users SET name=? WHERE id=? ''', (Value,UserID))
            elif UserAttribute == self.UserAttribute.Phone and self.IsPhoneValid(Value):
                self._db.cursor().execute('''UPDATE users SET phone=? WHERE id=? ''', (self.IsPhoneValid(Value),UserID))
            elif UserAttribute == self.UserAttribute.Password:
                self._db.cursor().execute('''UPDATE users SET password=? WHERE id=? ''', (Value,UserID))
            else: 
                return False
            self._db.commit()
            return True
        return False
    
    def GetTotalUsers(self):
        """Gets the total number of users.
        
        :returns: int: The total number of user accounts in the database.
        
        """
        return self._db.cursor().execute('''SELECT Count() FROM users''').fetchone()[0]
    
    def GetMostCommonName(self):
        """Gets the most common name used for user accounts in the database.
        
        :returns: str: The most common name used in the database.
        
        """
        if int(self.GetTotalUsers()) == 0:
            return "N/A"
        return self._db.cursor().execute('''SELECT name, Count(name) AS cnt FROM users GROUP BY name ORDER BY cnt DESC''').fetchone()[0]
    
    def GetSumOfIDs(self):
        """Gets the sum of all the user account IDs.
        
        :returns: int: The sum of all user account IDs in the database.
        
        """
        if int(self.GetTotalUsers()) == 0:
            return "N/A"
        return self._db.cursor().execute('''SELECT Sum(id) FROM users''').fetchone()[0]

    def GetUptime(self):
        """Gets the current uptime for this database.
        
        :returns: timedelta: The current length of time the database has been running in memory.
        
        """
        return datetime.now() - self.StartedTime
    
    @staticmethod
    def IsEmailValid(Email):
        """Determines if an Email address is valid.
        
        :param Email str: The email address to validate.
        :returns: str: The validated email address if valid, False if the provided email address was invalid.
        
        """
        Email = Email.lower()
        if re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', Email):
            return Email
        return False

    @staticmethod
    def IsPhoneValid(Phone):
        """Determines if a phone number is valid.
        
        :param Phone str: The phone number to validate.
        :returns: str: The validated phone number if valid, False if the provided phone number was invalid.
        
        """
        SanitizedValue = re.sub('[^0-9]','', Phone)
        if len(SanitizedValue) == 10:
            return SanitizedValue
        return False
    

