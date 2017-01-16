import pandas as pd
import urllib.request
import json

from CODES import ID_CODE_TREND_UPWARDS, ID_CODE_TREND_DOWNWARDS

print("Reading data from CSV...")
df = pd.read_csv('historical_balance.csv', parse_dates=[1])
print("Done!")


# print(df.dtypes)

########### PARAMETERS HERE ############

microservice_address= 'localhost'  # this is the address of the microservice.
                                   # Change with relevant address if not running on localhost
# acc_no = 1784947085
acc_no = 3209209351
# acc_no = 4148399665
# acc_no = 17584507766226

#######################


df_1 = df[df.account_num == acc_no]

print("Populating data for account number %s" % acc_no)
for index, row in df_1.iterrows():
    response = urllib.request.urlopen("http://{address}/add?" \
                                      "account_no={account_no}&date={date}"
                                      "&ledger_balance={ledger_balance}&cleared_balance={cleared_balance}".format(
        address=microservice_address,
        account_no=acc_no,
        date=row['date'].strftime('%Y-%m-%d'),
        ledger_balance=row['ledger_balance'],
        cleared_balance=row['cleared_balance']))

    message = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))
    # print(message)
    message_id_code = int(message['ID_CODE'])

    if message_id_code == ID_CODE_TREND_UPWARDS:
        print("On Date: %s    Trend upwards" % row['date'])

    if message_id_code == ID_CODE_TREND_DOWNWARDS:
        print("On Date: %s    Trend downwards" % row['date'])



print("Data successfully populated!")
print("Visualize it here:\n   http://{address}/visualize?account_no={account_no}"
          .format(
                    address=microservice_address,
                    account_no=acc_no)
                )
