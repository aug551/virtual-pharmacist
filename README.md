# Virtual Pharmacist Chatbot
## About
This virtual agent was created to test the capabilities of OpenAI gpt-3.5 as an assistant to seek advice on medications and supplements as well as handling prescription orders.

This prototype is created to function on the Python console with the plan to be used in a chat application on the browser, then on mobile.

### Version History
- v0.7 - Prototype (console app)
- v1.0 - First Release --- ***Work in Progress***

## Setup
### Requirements
The virtual agent runs on Mac OS X, Windows, or Linux.

Python dependencies (also in requirements.txt)
- Python 3.6+
- OpenAI 
- Pandas
- Python-dotenv
- Asyncio
- Scikit-learn

### Generate OpenAI API key
Before generating an API key create a file named ***.env*** at the root of the project.

Copy and paste the following onto the ***.env*** file:

```sh
OPENAI_ORGANIZATION_ID=<Organization-ID>
OPENAI_API_KEY=<API-secret-key>
```

1. Navigate to the [OpenAI platform (platform.openai.com)](https://platform.openai.com/)
2. Create an account or log in
3. At the top-right, click on your avatar and select *View API keys*
4. Create a new secret key and give it any name
5. Replace the *\<API-secret-key\>* from the ***.env*** file created earlier with the newly created secret key
6. Click on your avatar at the top-right again, this time selecting *Manage account*
7. Replace the *\<Organization-ID\>* from the ***.env*** file created earlier with your *Organization ID*


## Getting Started
### Prototype version - Console Interface
Since this is a prototype version, the only UI is from the console. You can start the program by running the ***`main.py`*** file.

From the root directory, run:
`python3 ./main.py`

Currently, there are 4 conversation options:
| *Scenario* | *Description* | *Example input* |
| ---------- | ------------ | --------- |
| New order | This workflow handles ordering medication from a prescription. | *I would like to place a prescription order for pickup.* |
| Order status | This workflow handles any queries to check the status of an order | *I have an order and I would like to check its status.* | 
| Medication information | This workflow will prompt Openai's chat completion model to give information about a particular supplement or medication | *I have a bad headache. Any recommendations for medication?* |
| Exit | This workflow will stop the chatbot. Alternatively, you can use a keyboard interrupt such as `Ctrl-C` to exit the program. | *Exit* |
  

***Note:***  *Scenarios 1 and 2 will prompt the user to input a Medicare number, date of birth, and either a prescription id or an order id. The data it checks from are all stored under* `/data/mock/*.csv` *The plan is to eventually integrate with a database for storing and retrieving data.*

## TODO
### User Interface
Console applications are not client-facing and are mainly used for prototyping and development. To fully complete the first release (v1.0), a user interface needs to be created.

### Database Integration
Currently, we are using CSV files to read and write information from. Integrating with a database is crucial for making this a fully-fledged application.

### ChatGPT/Intent classification fine-tuning
When ChatGPT is asked questions that are unrelated to supplements and medications - such as *what is electromagnetic interference?* - It will answer that question instead of giving an error message.

### Use cases
The following use cases are in the order of priority:
| Number | Use case |
| ------ | -------- |
| UC 01 | *As a user, I would like to interact with the virtual pharmacist on the browser.* |
| UC 02 | *As a business, I would like the chatbot to only respond to the four scenarios depicted above to conserve OpenAI tokens and to better market our products.* |
| UC 03 | *As a process owner, I need to integrate a database to properly store and retrieve information so that user information can be better secured.* |
| UC 04 | *As a user on-the-go, I would like to interact with the virtual pharmacist on a mobile application for quick queries.* |
