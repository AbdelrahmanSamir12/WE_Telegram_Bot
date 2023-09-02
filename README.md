# Description
WE_Telegram_Bot  is a Python script that allows users to monitor their internet usage data from Telecom Egypt "WE".\
It provides both a standalone usage data retrieval functionality and the option to integrate with a Telegram bot for automated usage summaries every 2 hours and on-demand data checks.\

The provided code fetches internet usage data from Telecom Egypt's API and generates a usage summary that includes the following information:
1. **Available Data**: The amount of available data in gigabytes (GB) from your total quota.
2. **Total Quota**: The total data quota you have subscribed to in GB.
3. **Used Data**: The amount of data you have already used in GB.
4. **Usage Percentage**: The percentage of your data quota that you have used.
5. **Remaining Days**: The number of days remaining until your data quota resets for renewal.

Here's an example of what the usage summary when printed:
``` 
___________________________
Available : 236.27 GB from 255.0 GB
Used : 18.73 GB
Usage percentage : 7.34 %
Remaining days : 27 days
___________________________
```


# Usage Instructions
**1. Standalone Usage Data Retrieval**

- To fetch internet usage data without using the Telegram bot, you can create an instance of the WE_API class.
- Provide the required credentials (login_phone, phone, and password) when initializing the WE_API object.
- Call the fetch_data() method to retrieve and print your internet usage summary.
  
``` python
we_account_data_fetcher = WE_API(login_phone, phone_number, we_account_password)
we_account_data_fetcher.fetch_data()
```

**2. Telegram Bot Integration**
- To use the Telegram bot for automated usage summaries and on-demand checks, create an instance of the TelegramBot class.
- Provide the required Telegram bot token, login_phone, password, phone number, and your Telegram user ID when initializing the TelegramBot object.
- Call the StartTelegramBot() method to initiate the bot functionality.
``` python
telegram = TelegramBot(telegram_bot_token, login_phone, we_account_password, phone_number, telegram_user_id)
telegram.StartTelegramBot()
```

**3. Telegram Bot Commands**
- The bot supports a "/check" command that allows you to manually check and receive your current internet usage summary.


# Dependencies
Install the external dependencies using.\
`pip install -r requirements.txt`

# Configuration
- Create a ".env" file.
- Store your Telegram bot token, Telegram user ID, login phone, phone number, and password in the ".env" file.
  
Here's the content of the ".env" file.
``` env
TelegramBotToken=YOUR_BOT_TOKEN
TelegramUserID=YOUR_USER_ID
LoginPhone=YOUR_LOGIN_PHONE
Phone=YOUR_PHONE_NUMBER
Password=YOUR_WE_ACCOUNT_PASSWORD
```
Note: 
- if you don't want the Telegram bot functionalty only store your login phone,phone number and password in the ".env" file.
- If the account number you want to retrieve data from is the phone number used for logging in, ensure that LoginPhone and Phone are identical. " as some accounts have several numbers ".


  
