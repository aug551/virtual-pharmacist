import pandas as pd


class OrderHandler:
    """
    Build Scenario: The chatbot should have at least 4 conversational scenarios

    This class is used as a helper to integrate with openai API.
    It contains 2/4 conversational scenarios:

    1. The user asks to create an pickup order for their medication using their medicare number and prescription number
    2. The user asks to check on the status of their order

    ....


    Methods
    -------
    askForInfo(req_type: str) -> {"medicare_number": str, "dob": str, "prescription_number": str } | {"medicare_number": str, "dob": str, "order_id": str}
        Prompts the user to enter their medicare number, date of birth and prescription or order number. This is used for both scenarios to gather user information.

    getClient(medicare_number: str, dob) -> {"medicare_number": str, "firstname": str, "lastname": str, "dob": str, "gender": str, "phonenumber": str} | None
        Method that queries the client based on medicare_number and dob. Returns None if not found and the client row if found.

    getOrder(orderid: str) -> {"orderid": str, "medicare_number": str, "prescriptionid": str, "order_state": str} | None
        Method that queries the order based on the order_id. This method is preceded by "getClient" to verify if the client ordering matches the client in the order row.

    getOrderStatus()
        Uses the askForInfo method to get information on the user's order. When the method has the information, it prints the status of the order, or an error if not found.

    getPrescription(prescription_number: str, client: Any) -> {"prescriptionid": str, "supplementid": str, "clientid": str, "datecreated": str, "quantity": str} | None
        This method queries the prescriptions based on the prescriptionid. It returns either the prescription row or None if not found.


    newOrder()
        Starts the workflow for creating a new order. 
        The method will use askForInfo to get user and prescription information, then it will validateInfo to see if the user or prescription is valid.
        If it is, the method will return the new order number and will insert the new order in the orders_mock.csv file.

    validateInfo(medicare_number: str, dob: str, prescription_number: str | None, orderid: str | None) -> 
    {"orderid": str, "medicare_number": str, "prescriptionid": str, "order_state": str} | True
        This method will check if the user information entered is correct and check if the user has a valid associated prescription to order from 
        or if the orderid is associated with an order row.
    
    """

    def __init__(self) -> None:
        
        """
        Attributes
        ----------
        self.clients: DataFrame
            DataFrame containing all users from the clients_mock.csv file.
        self.orders: DataFrame
            DataFrame containing all orders from the orders_mock.csv file. 
        self.prescriptions: DataFrame
            DataFrame containing all prescriptions from the prescriptions_mock.csv file. 
        self.supplements: DataFrame
            DataFrame containing all supplements from the supplements_mock.csv file. 
        self.client_info: {"medicare_number": str, "firstname": str, "lastname": str, "dob": str, "gender": str, "phonenumber": str} | None
            When client information is entered and validated, this variable will contain the client information, otherwise it will be None.

        """

        self.clients = pd.read_csv("./data/mock/clients_mock.csv", delimiter="|")
        self.orders = pd.read_csv("./data/mock/orders_mock.csv", delimiter="|")
        self.prescriptions = pd.read_csv("./data/mock/prescriptions_mock.csv", delimiter="|")
        self.supplements = pd.read_csv("./data/mock/supplements_mock.csv", delimiter="|")
        self.client_info = None

    def getClient(self, medicare_number, dob):
        """
        Method that queries the client based on medicare_number and dob.

        Parameters
        ----------
        medicare_number: str
            The medicare number of the client to query with.
        dob: str
            The client's date of birth using the format (yyyy-mm-dd). This is used to verify the user's identity.

        Returns
        -------
        Either None type or client Row: { "medicare_number": str, "firstname": str, "lastname": str, "dob": str, "gender": str, "phonenumber": str }

        """
        client = self.clients[
            (self.clients["medicare_number"] == medicare_number)
            & (self.clients["date_of_birth"] == dob)
        ]

        if client.empty:
            return None
        else:
            return client

    def getPrescription(self, prescription_number, client):
        """
        Method that queries the prescriptions based on prescription_number and client information.

        Parameters
        ----------
        prescription_number: str
            The prescription number of the prescription to query the self.prescriptions DataFrame with.
        client: str
            The client DataFrame row ({ "medicare_number": str, "firstname": str, "lastname": str, "dob": str, "gender": str, "phonenumber": str })

        Returns
        -------
        None: None type | Row: containing prescription information
        
        """
        prescription = self.prescriptions[
            (self.prescriptions["prescriptionid"] == int(prescription_number))
            & (self.prescriptions["clientid"] == client.iloc[0]["medicare_number"])
        ]

        if prescription.empty:
            return None
        else:
            return prescription

    def getOrder(self, orderid):
        """
        Method that queries the orders based on orderid.

        Parameters
        ----------
        orderid: str
            The orderid to look with.
        
        Returns
        -------
        None: None type | Row: containing the order information
        
        """
        order = self.orders[self.orders["orderid"] == int(orderid)]

        if order.empty:
            return None
        else:
            return order

    def validateInfo(self, medicare_number, dob, prescription_number, orderid):
        """
        Method that verifies if the information that the user entered is the correct information.

        Parameters
        ----------
        medicare_number: str
            The medicare number of the client.
        dob: str
            The date of birth of the client with the format (yyyy-mm-dd)
        prescription_number: str | None
            The prescription number to validate.
            If this value is None, the method will validate orders instead
        orderid: str | None
            The orderid to validate.
            If this value is None, the method will validate prescriptions instead.

        Returns
        -------
        Row: containing the order information | True: if the workflow is for prescriptions

        Raises
        ------
        1. Exception: When the client cannot be found using the "getClient" function
        2. Exception: When the prescription cannot be found using the "getPrescription" function
        3. Exception: When the order cannot be found using the "getOrder" function.
        
        """
        client = self.getClient(medicare_number, dob)

        if client is None:
            raise Exception(
                "The file could not be found in the system. Please try a different medicare number."
            )

        if prescription_number is not None:
            prescription = self.getPrescription(prescription_number, client)

            if prescription is None:
                raise Exception(
                    "The prescription could not be found with this prescription number."
                )

        if orderid is not None:
            order = self.getOrder(orderid)

            if order is None:
                raise Exception(
                    f"The order with the id {orderid} could not be found. Please try a different one."
                )

            return order.iloc[0]

        return True

    def askForInfo(self, req_type):
        """
        Prompts the user to enter their information

        Parameters
        ----------
        req_type: str
            If the request type is to order medication, the user will be prompted for prescripton information,
            otherwise, the user will be prompted to enter order number to check order status.
        
        Returns
        -------
        {"medicare_number": str, "dob": str, "prescription_number": str | "orderid": str}
            Returns the user input.
        
        """
        print("In order to process your request, we need the following information: ")
        if self.client_info is None:
            medicare_number = input("1. Medicare number: ")
            dob = input("2. Date of birth (yyyy-mm-dd): ")
        else:
            medicare_number = self.client_info["medicare_number"]
            dob = self.client_info["dob"]
        if req_type == "new":
            prescription_number = input("3. Prescription number: ")

            return {
                "medicare_number": medicare_number,
                "dob": dob,
                "prescription_number": prescription_number,
            }
        else:
            orderid = input("3. Order number: ")
            return {"medicare_number": medicare_number, "dob": dob, "orderid": orderid}

    def newOrder(self):
        """
        This method will prompt the user for their information using askForInfo.
        Then their information will be validated using validateInfo.
        If the information is successfully validated, a new order will be inserted in the orders_mock.csv file.
        
        Exceptions
        ----------
        e: Exception
            Prints the errors that might be raised throughout the whole process
        
        """

        client_info = self.askForInfo("new")

        try:
            if self.validateInfo(
                client_info["medicare_number"],
                client_info["dob"],
                client_info["prescription_number"],
                None,
            ):
                self.client_info = {
                    "medicare_number": client_info["medicare_number"],
                    "dob": client_info["dob"],
                }
                new_order = {
                    "orderid": len(self.orders) + 1,
                    "medicare_number": client_info["medicare_number"],
                    "prescriptionid": client_info["prescription_number"],
                    "order_state": "1",
                }

                # TODO: This needs to be a proper database insert
                new_df = pd.DataFrame([new_order])
                self.orders = pd.concat([self.orders, new_df], ignore_index=True)

                print(
                    f"Order Successful! The order number is: {new_order['orderid']}\n"
                )

                self.orders.to_csv(
                    "./data/mock/orders_mock.csv", 
                    sep="|",
                    encoding="utf-8",                 
                    index=False,
                )

        except Exception as e:
            print(e)

    def getOrderStatus(self):
        """
        This method asks for user input will display the state of the medication order.

        Exceptions
        ----------
        e: Exception
            Prints the errors that might be raised throughout the whole process
        
        """
        client_info = self.askForInfo("status")

        try:
            order = self.validateInfo(
                client_info["medicare_number"],
                client_info["dob"],
                None,
                client_info["orderid"],
            )

            if int(order["order_state"]) == 1:
                print("Your medication order is pending.")
            elif int(order["order_state"]) == 2:
                print("Your medication order is ready for pick up")
            elif int(order["order_state"]) == 3:
                print("Your medication order has already been picked up")
        except Exception as e:
            print(e)
