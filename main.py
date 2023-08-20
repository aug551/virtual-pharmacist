from classes.OrderHandler import OrderHandler
from classes.Chatbot import Chatbot
from classes.IntentClassifier import IntentClassifier
from datetime import datetime
import asyncio

order_handler = OrderHandler()
chatbot = Chatbot()

userInputs = []
botResponses = []


def logAll():
    """
    This function will log all user inputs and all gpt-3 responses to the files "user_inputs.log" and "bot_responses.log" respectively.
    This is called at the end of the main function when the user exits the application.
    """

    # Open the files users_input.log and bot_responses.log for appending
    # Then, write all user inputs and bot responses to those files
    with open("./logs/user_inputs.log", "a") as file1:
        file1.write("\n".join(userInputs))
        file1.write("\n")
    with open("./logs/bot_responses.log", "a") as file2:
        file2.write("\n".join(botResponses))
        file2.write("\n")

def processIntent(input):
    """
    This function creates the IntentClassifier object to predict user intent from the user input

    Parameters
    ----------
    input: str
        User input to predict intent from.

    Returns
    -------
    predicted_intent | "bot_help": str
        The predicted intent. Fallback is "bot_help"
    """

    # Create IntentClassifier object
    classifier = IntentClassifier()

    # Predict intent for user input using predict_intent method
    predicted_intent = classifier.predict_intent(input)

    if predicted_intent == "order" or predicted_intent == "status" or predicted_intent == "exit":
        return predicted_intent
    else:
       return "bot_help"



async def main():
    """
    Main workflow of the chatbot
    """

    # Prompt gpt-3 for a greeting as a pharmacist chatbot
    greeting = await chatbot.getGreeting() + "\n"
    print(greeting)

    # We want to catch KeyboardInterrupt exceptions to save the logs.
    try:
        # Workflow will loop until exited
        while True:
            user_input = input("User input: ")

            # Appending the logs to the variable to be saved later
            userInputs.append(str(datetime.now()) + ": " + user_input)

            intent = processIntent(user_input)

            try:
                if intent == "order":
                    order_handler.newOrder()

                elif intent == "status":
                    order_handler.getOrderStatus()

                elif intent == "bot_help":
                    response = await chatbot.get_bot_response(
                        {"role": "user", "content": user_input}
                    )
                    print(response)
                    # Appending the logs to the variable to be saved later
                    botResponses.append(str(datetime.now()) + ": " + response)

                elif intent == "exit":
                    # Force an exception to run the logAll function
                    raise (KeyboardInterrupt)

                # This print statement can be added at the end of each workflow.
                # When testing it was quite annoying, but if you want to enable it, this can be enabled here.
                # print("\nIs there anything else I can help you with?")

            except Exception as e:
                print(e)
    except KeyboardInterrupt:
        logAll()


if __name__ == "__main__":
    # We need to run the main function asynchronously because we are using an external connection with an API
    asyncio.run(main())

