from collections import Counter
import db, random, string, datetime

class TestDB:

    Database = db.DB()
    TestUsers = [["Carl", "111-111-1111", "carl@yahoo.com", "drgaf65s41f6s"], ["Jenni J.", "222-314-1789", "jenni@outlook.com", "setgg48596"], ["Rainbow Sunshine", "999-999-9999", "rainbowsunshine@hotmail.com", "6+rftyu5512"], ["Carl", "914-867-5309", "helloworld@live.com", "fsedg8458f"]]

    def test_IsEmailValid(self):
        ValidEmails = ["johndoe@example.com", "humanoid567@yahoo.com", "HeLlOw0rLd@gmail.com", "ALLC4PSMAN@outlook.com", "dsfsfsDFGDFGdfgsegsdgfsdg@HJghjGjhGBjhGBhGJkGhGJHUGhGGHJgJg.com"]
        InvalidEmails = ["user#@bad.com", "abc123", "@.com", "&*$%^&(*@()%()#&%)%#.com", "6", '']
        for x in ValidEmails:
            assert(db.DB.IsEmailValid(x).islower())
        for y in InvalidEmails:
            assert(not db.DB.IsEmailValid(y))
    
    def test_IsPhoneValid(self):
        ValidPhoneNumbers = ['555-777-8969', '1111111111', '(845) 678-9760', '999.999.9999', '800-464-7890']
        InvalidPhoneNumbers = ['55555555555', '23', 'dsd', '456123789', '']
        for x in ValidPhoneNumbers:
            assert(db.DB.IsPhoneValid(x).isnumeric())
        for y in InvalidPhoneNumbers:
            assert(not db.DB.IsPhoneValid(y))
    
    def test_AddAndFindUser(self):
        for User in self.TestUsers:
            self.Database.AddUser(User[0], User[1], User[2], User[3])
            assert self.Database.FindUser(self.Database.UserAttribute.Name, User[0])
            assert self.Database.FindUser(self.Database.UserAttribute.Phone, User[1])
            assert self.Database.FindUser(self.Database.UserAttribute.Email, User[2])
    
    def GenerateRandomString(self, Length = 16):
        result = ""
        for x in range(Length):
            result += random.choice(string.ascii_lowercase + string.digits)
        return result
    
    def GenerateRandomName(self):
        result = f'{self.GenerateRandomString()} {self.GenerateRandomString()}'
        if self.Database.FindUser(self.Database.UserAttribute.Name, result):
            return self.GenerateRandomString()
        return result
    
    def GenerateRandomEmail(self):
        RandomUser = self.GenerateRandomString(random.randint(1, 16))
        RandomDomain = self.GenerateRandomString(random.randint(1, 16))
        RandomEmail = f"{RandomUser}@{RandomDomain}.com"
        if self.Database.FindUser(self.Database.UserAttribute.Email, RandomEmail):
                return self.GenerateRandomEmail()
        return RandomEmail

    def GenerateRandomPhone(self):
        Result = ""
        for x in range(10):
            Result += f"{random.randint(0, 9)}"
        if self.Database.FindUser(self.Database.UserAttribute.Phone, Result):
            return self.GenerateRandomPhone()
        return Result
    
    def test_DoesUserExist(self):
        for User in self.TestUsers:
            assert self.Database.DoesUserExist(User[2])
        for x in range(5):
            assert not self.Database.DoesUserExist(self.GenerateRandomEmail())

    def test_AttemptLogIn(self):
        for User in self.TestUsers:
            assert self.Database.AttemptLogIn(User[2], User[3])
        for x in range(5):
            assert not self.Database.AttemptLogIn(self.GenerateRandomEmail(), self.GenerateRandomString())
    
    def GetIDFromEmail(self, Email):
        return self.Database.FindUser(self.Database.UserAttribute.Email, Email)[0]
    
    def GetIDFromPhone(self, Phone):
        return self.Database.FindUser(self.Database.UserAttribute.Phone, Phone)[0]
    
    def GetIDFromName(self, Name):
        return self.Database.FindUser(self.Database.UserAttribute.Name, Name)[0][0]

    def test__DoesPasswordMatch(self):
        for User in self.TestUsers:
            assert self.Database._DoesPasswordMatch(self.GetIDFromEmail(User[2]), User[3])
            assert not self.Database._DoesPasswordMatch(self.GetIDFromEmail(User[2]), self.GenerateRandomString())

    def test_ChangeUserAttribute(self):
        for User in self.TestUsers:
            ID = self.GetIDFromEmail(User[2])
            for x in range(5):
                randomEmail = self.GenerateRandomEmail()
                randomName = self.GenerateRandomName()
                randomPhone = self.GenerateRandomPhone()
                self.Database.ChangeUserAttribute(ID, self.Database.UserAttribute.Email, randomEmail, User[3])
                assert self.GetIDFromEmail(randomEmail) == ID
                self.Database.ChangeUserAttribute(ID, self.Database.UserAttribute.Phone, randomPhone, User[3])
                assert self.GetIDFromPhone(randomPhone) == ID
                self.Database.ChangeUserAttribute(ID, self.Database.UserAttribute.Name, randomName, User[3])
                assert self.GetIDFromName(randomName) == ID
                assert not self.Database.ChangeUserAttribute(ID, self.Database.UserAttribute.Email, self.GenerateRandomString(), User[3])
                assert not self.Database.ChangeUserAttribute(ID, self.Database.UserAttribute.Phone, self.GenerateRandomString(), User[3])
            self.Database.ChangeUserAttribute(ID, self.Database.UserAttribute.Name, User[0], User[3])
            self.Database.ChangeUserAttribute(ID, self.Database.UserAttribute.Phone, User[1], User[3])
            self.Database.ChangeUserAttribute(ID, self.Database.UserAttribute.Email, User[2], User[3])
    
    def test_GetTotalUsers(self):
        assert self.Database.GetTotalUsers() == len(self.TestUsers)
    
    def test_GetMostCommonName(self):
        Names = []
        for User in self.TestUsers:
            Names.append(User[0])
        assert self.Database.GetMostCommonName() == Counter(Names).most_common(1)[0][0]
    
    def test_GetSumOfIDs(self):
        IDSum = 0
        for User in self.TestUsers:
            IDSum += self.GetIDFromEmail(User[2])
        assert self.Database.GetSumOfIDs() == IDSum
    
    def test_GetUptime(self):
        assert type(self.Database.GetUptime()) is datetime.timedelta
    
    def test_DeleteUser(self):
        for User in self.TestUsers:
            ID = self.GetIDFromEmail(User[2])
            for x in range(5):
                assert not self.Database.DeleteUser(ID, self.GenerateRandomString)
            assert self.Database.DeleteUser(ID, User[3])

            
