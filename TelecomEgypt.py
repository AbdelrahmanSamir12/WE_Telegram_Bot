import requests
import json
import schedule
import telebot
from decouple import config
import time
from threading import Thread
import PasswordEncreption


"""
you can use this class to fecth internet usage data without needing a 
telegram bot
"""
class WE_API():
    def __init__(self,login_phone,phone,password):
        self.login_phone = login_phone
        self.phone = phone
        self.password = password  # plain Text

        #Encrypting the password using WE encryption algorithm
        self.Encreptor = PasswordEncreption.WEPasswordEncryptor()
        self.password = self.Encreptor.encrypt(self.password)


    def fetch_data(self):

        """
        this function handles the fetching the data from Telecom Egypt API
        """
        constant_header = {
            "Host": "api-my.te.eg",
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/537.36",
            "Origin": "https://my.te.eg",
            "Referer": "https://my.te.eg/"
        }

        # fetching the a login jwt "JASON web token" to use it to fetch login data
        Login_Token_request = requests.get("https://api-my.te.eg/api/user/generatetoken?channelId=WEB_APP", headers=constant_header, verify=True)
        login_respond_data = json.loads(Login_Token_request.text)
        login_jwt = login_respond_data["body"]["jwt"]
        login_headers = constant_header
        login_headers["jwt"] = login_jwt
        login_headers["Content-Type"] = "application/json"
        login_headers["Content-Length"] = "145"



        # Retrieving user data along with the personal JWT to get access to internet usage information
        login_request_body = '{"header": {"msisdn": "%s","numberServiceType": "FBB","timestamp": "1674239839","locale": "en"},"body": {"password": "%s"}}' % (self.login_phone, self.password)
        login_respond = requests.post("https://api-my.te.eg/api/user/login?channelId=WEB_APP", headers = login_headers, data = login_request_body, verify = True)
        login_respond_data = json.loads(login_respond.text)
        jwt = login_respond_data["body"]["jwt"]
        self.customerID = login_respond_data["header"]["customerId"]
        

        # Updating the JWT in the header with the new one and then fetching the data related to internet usage.
        account_data_headers = login_headers
        account_data_headers["jwt"] = jwt
        json_body = '{"header": {"customerId": "%s","msisdn": "%s","numberServiceType": "FBB","locale": "en"}}' % (self.customerID,self.phone)
        account_data_headers["Content-Length"] = "99"
        account_data_responde = requests.post("https://api-my.te.eg/api/line/freeunitusage", headers = account_data_headers, data=json_body)

        # Creating a summary of the internet usage data.
        free_amount = json.loads(account_data_responde.text)["body"]["summarizedLineUsageList"][0]["freeAmount"]
        total_qouta = json.loads(account_data_responde.text)["body"]["summarizedLineUsageList"][0]["initialTotalAmount"]
        used_amount = json.loads(account_data_responde.text)["body"]["summarizedLineUsageList"][0]["usedAmount"]
        use_percentage = json.loads(account_data_responde.text)["body"]["summarizedLineUsageList"][0]["usagePercentage"]
        remaining_days = json.loads(account_data_responde.text)["body"]["detailedLineUsageList"][0]["remainingDaysForRenewal"]

        we_message = f'Available : {free_amount} GB from {total_qouta} GB \nUsed : {used_amount} GB \nUsage percentage : {use_percentage} %\nRemaining days : {remaining_days} days'


        print("___________________________\n")
        print(we_message)
        print("___________________________")


        responde = {
            "available" : free_amount,
            "total" : total_qouta,
            "used" : used_amount,
            "percentage" : use_percentage,
            "remaining": remaining_days
        }

        
        return responde
    
class TelegramBot():
    def __init__(self, api_token, login_phone, password, phone, telegram_id):
        self.api_token = api_token
        self.telegram_id = telegram_id
        self.login_phone = login_phone
        self.phone = phone
        self.password = password
        self.bot = telebot.TeleBot(api_token)
        self.WeDataFetcher = WE_API(login_phone,phone,password)

    def send_summary(self, data):

        # Handling sending the Summary massege the the telegram account
        we_message = f'Available : {data["available"]} GB from {data["total"]} GB \n Used : {data["used"]} GB \nUsage percentage : {data["percentage"]} %\nRemaining days : {data["remaining"]} days'
        self.bot.send_message(self.telegram_id, we_message)
        

    def check_and_send(self):

        # Initiating communication with the API, retrieving usage information, and subsequently forwarding it to the user.
        data = self.WeDataFetcher.fetch_data()
        self.send_summary(data)

    def scheduled(self):

        #Managing the automated process of sending scheduled usage summaries to the user.
        schedule.every(2).hours.do(self.check_and_send)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def StartTelegramBot(self):

        #handles the whole proccess of the bot
        self.check_and_send()
        @self.bot.message_handler(commands=["check"])
        def check(message):
            self.check_and_send()

        """
        Implementing multi-threading to enable the script to simultaneously manage user commands
        and scheduled usage summary sent to the user.
        """
        send_thread = Thread(target=self.scheduled)
        send_thread.start()
        
        command_thread = Thread(target=self.bot.polling)
        command_thread.start()

    
    


def main():
  
    telegram_user_id = int(config('TelegramUserID'))
    telegram_bot_token = config('TelegramBotToken')
    login_phone = config('LoginPhone')
    phone_number = config('Phone')
    we_account_password = config('Password') 

    # Fetching internet usage data without using a Telegram bot
    we_account_data_fetcher = WE_API(login_phone,phone_number,we_account_password)
    we_account_data_fetcher.fetch_data()

    # Using the Telegram bot
    telegram = TelegramBot(telegram_bot_token,login_phone,we_account_password,phone_number,telegram_user_id)
    telegram.StartTelegramBot()





if __name__ == "__main__":
    main()


