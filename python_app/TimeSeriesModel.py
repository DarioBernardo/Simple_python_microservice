import pandas as pd

from CODES import *


class TimeSeriesModel:

    def __init__(self):
        self.ts_dict = {}


    def add_point_to_ts(self, account_no, date, ledger_balance, cleared_balance):
        df = self.ts_dict.get(account_no, pd.DataFrame())
        df = df.append({'date': date, 'ledger_balance':ledger_balance, 'cleared_balance':cleared_balance}, ignore_index=True)
        df['ewm'] = df.cleared_balance.ewm(com=0.8).mean()
        df['ma'] = df.cleared_balance.rolling(window=35).mean()
        self.ts_dict[account_no] = df

        if len(df) > 2:
            last_two_rows = df.tail(2)
            b_ewm = last_two_rows.iloc[0]['ewm']
            b_ma = last_two_rows.iloc[0]['ma']
            a_ewm = last_two_rows.iloc[1]['ewm']
            a_ma = last_two_rows.iloc[1]['ma']

            if b_ewm < b_ma and a_ewm > a_ma:
                return ID_CODE_TREND_UPWARDS

            if b_ewm > b_ma and a_ewm < a_ma:
                return ID_CODE_TREND_DOWNWARDS

        return ID_CODE_NO_MSSAGE

    def get_data_for_accout(self, account_no):
        return self.ts_dict.get(account_no, pd.DataFrame(columns=['date', 'ledger_balance', 'cleared_balance']))