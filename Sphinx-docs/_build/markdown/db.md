# db module


### _class_ db.DB(FilePath=':memory:')
Bases: `object`

A local database to demonstrate a login system.


#### AddUser(Name, Phone, Email, Password)
Adds a user account to the current database.


* **Parameters**

    
    * **str** (*Password*) – The name of the new user.


    * **str** – The phone number of the new user.


    * **str** – The email address of the new user.


    * **str** – The password the new user selected for their account.



* **Returns**

    bool: True if the account creation was successful, False if it was unsuccessful.



#### AttemptLogIn(Email, Password)
Attempts to log in the user.


* **Parameters**

    
    * **str** (*Password*) – The email address for the user account.


    * **str** – The password used to try logging in.



* **Returns**

    int: The user account ID if the log in was successful, False if the user account does not.



#### ChangeUserAttribute(UserID, UserAttribute, Value, Password)
Changes an attribute about a user.


* **Parameters**

    
    * **int** (*UserID*) – The ID for the user account.


    * **UserAttribute** (*UserAttribute*) – The attribute to change about the user account.


    * **str** (*Password*) – The new value for the specified attribute.


    * **str** – The password used for the user account.



* **Returns**

    bool: True if the change was successful, False if the user account does not.



#### DeleteUser(UserID, Password)
Deletes a specified user.


* **Parameters**

    
    * **int** (*UserID*) – The ID of the user account to delete.


    * **str** (*Password*) – The password used for the user account.



* **Returns**

    bool: True if the account deletion was successful, False if it was not.



#### DoesUserExist(Email)
Finds if a user account exists.


* **Parameters**

    **str** (*Email*) – The email address for the user account.



* **Returns**

    bool: True if the user account exists in the database, False if the user account does not.



#### FindUser(UserAttribute, Input)
Finds a user account for a given input.


* **Parameters**

    
    * **UserAttribute** (*UserAttribute*) – The user attribute to use for searching for the user.


    * **str** (*Input*) – The string used to search for the user according to the UserAttribute.



* **Returns**

    list[str]: A list containing the ID, Name, Phone, and Email Address of the found user.



#### GetMostCommonName()
Gets the most common name used for user accounts in the database.


* **Returns**

    str: The most common name used in the database.



#### GetSumOfIDs()
Gets the sum of all the user account IDs.


* **Returns**

    int: The sum of all user account IDs in the database.



#### GetTotalUsers()
Gets the total number of users.


* **Returns**

    int: The total number of user accounts in the database.



#### GetUptime()
Gets the current uptime for this database.


* **Returns**

    timedelta: The current length of time the database has been running in memory.



#### _static_ IsEmailValid(Email)
Determines if an Email address is valid.


* **Parameters**

    **str** (*Email*) – The email address to validate.



* **Returns**

    str: The validated email address if valid, False if the provided email address was invalid.



#### _static_ IsPhoneValid(Phone)
Determines if a phone number is valid.


* **Parameters**

    **str** (*Phone*) – The phone number to validate.



* **Returns**

    str: The validated phone number if valid, False if the provided phone number was invalid.



#### PrintDebugTable()
Prints a table to the terminal window for debugging purposes.


#### _class_ UserAttribute(value)
Bases: `enum.Enum`

An enum used to describe different acceptable user attributes.


#### Email(_ = _ )

#### ID(_ = _ )

#### Name(_ = _ )

#### Password(_ = _ )

#### Phone(_ = _ )
