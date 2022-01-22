from fileinput import filename
from datetime import datetime
import sqlite3, enum, re, const

class DB:
    class UserAttribute(enum.Enum):
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
        Email = Email.lower()
        if self.FindUser(self.UserAttribute.Phone, Phone) or self.FindUser(self.UserAttribute.Email, Email):
            return False
        self._db.cursor().execute('''INSERT INTO users(name, phone, email, password) VALUES(?,?,?,?)''', (Name, Phone, Email, Password))
        self._db.commit()
    
    def PrintDebugTable(self):
        print(self._db.cursor().execute('''SELECT * FROM users''').fetchall())

    def FindUser(self, UserAttribute, Input):
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
        if self.FindUser(self.UserAttribute.Email, Email):
            return True
        return False

    def AttemptLogIn(self, Email, Password):
        User = self.FindUser(self.UserAttribute.Email, Email)
        if User:
            if self._DoesPasswordMatch(User[0], Password):
                return User[0]
        return False
    
    def _DoesPasswordMatch(self, UserID, Password):
        CorrectPassword = self._db.cursor().execute('''SELECT password FROM users WHERE id=?''', (UserID,)).fetchall()[0][0]
        return Password == CorrectPassword

    def DeleteUser(self, ID, Password):
        if self._DoesPasswordMatch(ID, Password):
            self._db.cursor().execute('''DELETE FROM users WHERE id=? ''', (ID,))
            self._db.commit()
            return True
        return False
    
    def ChangeUserAttribute(self, ID, UserAttribute, Value, Password):
        Value = Value.strip()
        if self._DoesPasswordMatch(ID, Password):
            if UserAttribute == self.UserAttribute.Email and self.IsEmailValid(Value):
                self._db.cursor().execute('''UPDATE users SET email=? WHERE id=? ''', (self.IsEmailValid(Value),ID))
            elif UserAttribute == self.UserAttribute.Name:
                self._db.cursor().execute('''UPDATE users SET name=? WHERE id=? ''', (Value,ID))
            elif UserAttribute == self.UserAttribute.Phone and self.IsPhoneValid(Value):
                self._db.cursor().execute('''UPDATE users SET phone=? WHERE id=? ''', (self.IsPhoneValid(Value),ID))
            elif UserAttribute == self.UserAttribute.Password:
                self._db.cursor().execute('''UPDATE users SET password=? WHERE id=? ''', (Value,ID))
            else: 
                return False
            self._db.commit()
            return True
        return False
    
    def GetTotalUsers(self):
        return self._db.cursor().execute('''SELECT Count() FROM users''').fetchone()[0]
    
    def GetMostCommonName(self):
        if int(self.GetTotalUsers()) == 0:
            return "N/A"
        return self._db.cursor().execute('''SELECT name, Count(name) AS cnt FROM users GROUP BY name ORDER BY cnt DESC''').fetchone()[0]
    
    def GetSumOfIDs(self):
        if int(self.GetTotalUsers()) == 0:
            return "N/A"
        return self._db.cursor().execute('''SELECT Sum(id) FROM users''').fetchone()[0]

    def GetUptime(self):
        return datetime.now() - self.StartedTime
    
    @staticmethod
    def IsEmailValid(Email):
        Email = Email.lower()
        if re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', Email):
            return Email
        return False

    @staticmethod
    def IsPhoneValid(Phone):
        SanitizedValue = re.sub('[^0-9]','', Phone)
        if len(SanitizedValue) == 10:
            return SanitizedValue
        return False
    

