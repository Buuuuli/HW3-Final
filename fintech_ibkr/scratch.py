
from ibapi.contract import Contract
from ibapi.order import Order
from fintech_ibkr import *
import pandas as pd





hostname = '127.0.0.1'
port = 7497
client_id = 116358 # can set and use your Master Client ID



# Contract object: STOCK
contract_stk = Contract()
contract_stk.symbol = "TSLA"
contract_stk.secType = "STK"
contract_stk.currency = "USD"
contract_stk.exchange = "SMART"
contract_stk.primaryExchange = "ARCA"

# Example LIMIT Order
lmt_order = Order()
lmt_order.action = "SELL"
lmt_order.orderType = "LMT"
lmt_order.totalQuantity = 100
lmt_order.lmtPrice = 1012

##### FA Accounts #####
# If you're a financial advisor (FA) then you're not finished creating your
# orders at this point because you need to answer the question: which account
# would you like to place the order on? All of them? Just one? Several? There
# are a few ways to do this, for example, by using GROUPS: https://www.interactivebrokers.com/en/software/advisors/topics/accountgroups.htm
# But probably the easiest way is to just pass in the ID of the account you
# want to use, like this:
lmt_order.account = 'DU5310097'
# Don't want to mess this one up because your clients all signed up for
# different strategies. You don't want to accidentally make trades for your
# wild options strategy using the account owned by your conservative, careful
# client who only trades index funds and dividend-paying stocks in the SP500!

# Place orders!
m = place_order(contract_stk, lmt_order)

df_file = pd.read_csv('C:\\submitted_orders.csv')

# find order account
order_account = lmt_order.account
# find order detail
order_ID = m['orderId'][0]

perm = m['perm_id'][0]
c = client_id
con_id = fetch_contract_details(contract_stk, hostname=hostname, port=port, client_id=client_id)['con_id'][0]
current_time = fetch_current_time()
smbol = contract_stk.symbol
action_buy_sell = lmt_order.action
size = lmt_order.totalQuantity
order_type = lmt_order.orderType
lmt_price = lmt_order.lmtPrice

df_file = df_file.append({'timestamp': current_time, 'order_id': order_ID, 'client_id': c, 'perm_id': perm,
                          'con_id': con_id, 'symbol': smbol, 'action': action_buy_sell,
                          'size': size, 'order_type': order_type, 'lmt_price': lmt_price}, ignore_index=True)

df_file.to_csv("C:\\submitted_orders.csv", index=False)