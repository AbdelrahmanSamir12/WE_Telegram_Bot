# Description
WE_Telegram_Bot  is a Python script that allows users to monitor their internet usage data from Telecom Egypt "WE".\
It provides both a standalone usage data retrieval functionality and the option to integrate with a Telegram bot for automated usage summaries and on-demand data checks.

# Usage Instructions
**1. Standalone Usage Data Retrieval**

- To fetch internet usage data without using the Telegram bot, you can create an instance of the WE_API class.
- Provide the required credentials (login_phone, phone, and password) when initializing the WE_API object.
- Call the fetch_data() method to retrieve and print your internet usage summary.

**2. Telegram Bot Integration**
- To use the Telegram bot for automated usage summaries and on-demand checks, create an instance of the TelegramBot class.
- Provide the required Telegram bot token, login_phone, password, phone number, and your Telegram user ID when initializing the TelegramBot object.
- Call the StartTelegramBot() method to initiate the bot functionality.

**3. Telegram Bot Commands**
- The bot supports a "/check" command that allows you to manually check and receive your current internet usage summary.


# Dependencies
install the external dependencies using.
`pip install -r requirements.txt`

# Configuration
Store your Telegram bot token, Telegram user ID, login phone, phone number, and password in the ".env" file.

```
TelegramBotToken=YOUR_BOT_TOKEN
TelegramUserID=YOUR_USER_ID
LoginPhone=YOUR_LOGIN_PHONE
Phone=YOUR_PHONE_NUMBER
Password=YOUR_WE_ACCOUNT_PASSWORD
```
Note: 
- if you don't want the Telegram bot functionalty only store your login phone,phone number and password in the ".env" file.
- If the account number you wish to retrieve data from is the phone number used for logging in, ensure that LoginPhone and Phone are identical. " as some accounts have several numbers ".


  
