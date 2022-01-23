# inputhandler module


### _class_ inputhandler.InputHandler()
Bases: `object`

A class to handle data input.


#### GetPassword(Message='Password')
Gets a password input without echoing characters to the terminal window.


* **Parameters**

    **str** (*Message*) – The message to display when asking the user for their password. (Default value = Password)



* **Returns**

    str: The password entered by the user.



#### GetValidInput(AcceptableResponses=None, InputBehavior=InputBehavior.Numeric, Message='Enter your Selection', FailedMessage='Invalid selection, please try again.', RetryOnFail=False)
Gets a valid input for a set of conditions.


* **Parameters**

    
    * **list****[****str****]** (*AcceptableResponses*) – A list of acceptable responses. If no list is provided, the function will not validate against this list. (Default value = None)


    * **InputBehavior** (*InputBehavior*) – Limits what type of input is allowed. (Default value = InputBehavior.Numeric)


    * **str** (*FailedMessage*) – The message to display when asking for input. (Default value = “Enter your Selection”)


    * **str** – The message to display when the input is invalid. (Default value = “Invalid selection, please try again.”)


    * **bool** (*RetryOnFail*) – If True, will try to get input from the user again if the input is invalid. If False, the function will return False if the user fails to enter valid data. (Default value = False)



* **Returns**

    str: The valid input from the user, or False if the user gives invalid data and RetryOnFail is False.



#### _class_ InputBehavior(value)
Bases: `enum.Enum`

An enum to describe different available input behaviors.


#### ConvertToLower(_ = _ )

#### Email(_ = _ )

#### Numeric(_ = _ )

#### PhoneNumber(_ = _ )

#### Raw(_ = _ )
