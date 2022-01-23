# cli module


### _class_ cli.CLI()
Bases: `object`

A command line application for interacting with a local database.


#### CreateNewUser()
Launches and drives a menu for creating a new user account.


#### DeleteAccount()
Launches and drives a menu for deleting the current user account.


#### DrawChangeValueMenu(UserAttribute)
Launches and drives a menu for changing an attribute of a logged in user account.


* **Parameters**

    **DB.UserAttribute** ([*UserAttribute*](db.md#db.DB.UserAttribute)) – The attribute to modify about a user account.



#### DrawMenu(Title, ListOfOptions, Details=None)
Draws a menu and returns the user’s selection.


* **Parameters**

    
    * **str** (*Details*) – The title of the menu to display.


    * **list****[****str****]** (*ListOfOptions*) – A list of options to display in the menu. Every option cooresponds to a possible return value.


    * **str** – A description the appears below the header. (Default value = None)



* **Returns**

    int: The number the user selected.



#### Exit()
Closes the application.


#### Launch()
Launches the program.


#### LogIn()
Launches and drives a menu to log into an existing user account.


#### LogOff()
Logs off the current user account.


#### LoggedInMenu()
Launches and drives the menu for logged in users.


#### PublicMainMenu()
Launches and drives the main menu for users not logged in.


#### ShowStatisticalInformation()
Launches and drives the statistical information menu.

### cli.ClearScreen()
Clears all text in the terminal window.


### cli.Notice(Message)
Displays a notice for a short amount of time before returning control to the user.


### cli.PrintHeader(title)
Clears the screen and prints a header for a menu.
