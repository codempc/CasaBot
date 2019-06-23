# Home Loan Chatbot (Casabot) with Dialogflow

41004: Analytics Capstone Project Deliverable, Autumn 2019.
Subject Coordinator: Supervisor: 
[Dr. Wei Liu](https://www.uts.edu.au/staff/wei.liu)

## About

Overseas Student Health Cover is the health insurance which allmost all of the international students in Australia have to purchase before applying for student visa. 
This chatbot intends to educate current and prospective international students in Australia about their OSHC cover, who are the providers and how much do they cost. 
(David)

## Demo
To see the working demo, click on the links
- <a href="https://bot.dialogflow.com/CasaBot" target="_blank">Dialogflow Instant Chat</a>
- <a href="m.me/400454180513269" target="_blank">Facebook Messenger</a>

## Prerequisites

To run the chatbot in you will need to have the following

 - [Google Drive Account](https://drive.google.com/drive/u/0/) - Google Sheet Setup.
 - [Free Dialogflow account](https://console.dialogflow.com)

## Installation

###  Step 1. Dialogflow

#### a. Create your free [Dialogflow] account (https://dialogflow.com/docs/getting-started/create-account)
#### b. Create the agent
![creating the agent](https://imgur.com/a/UATj2Tc)

#### c. Go to 'Settings' beside Agents list on top left below Dialogflow icon. Then, access the 'Export and Import' tab. Finally, click the 'Restore From Zip' button.
![import agent](https://imgur.com/a/518Hcf2)

#### d. Drop the cloned Casabot.zip files and then click the 'Restore' button.
![overwrite agent with Casabot zip files](https://imgur.com/a/Ww1qyg8)

#### e. Move to 'Fulfillment' tab on the center of the left navigation bar (the one with thunder-like icon). Enable the Webhook and then fill in the URL to handle the webhook requests (you can also use our default one, but you would need to use your own URL to modify the bot behaviour). 
![Webhook URL and Fulfilment Set up](https://imgur.com/a/FtGUp4X)

#### f. Go to 'Integrations' tab below 'Fulfillment' and choose any platform that you would like to integrate with.

### Step 2. GoogleSheets Setup 
