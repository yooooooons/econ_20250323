#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import pyupbit
import datetime
import pandas as pd
import numpy as np
import warnings
import traceback
import math
import random

warnings.filterwarnings('ignore')

#from scipy.signal import savgol_filter
#from scipy.signal import savitzky_golay

#import matplotlib.pyplot as plt


# In[2]:


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)


# In[3]:


# 투자 대상 코인 및 설정값



# Type_2

BTC_0_dic = {'type': 'type_2', 'coin_Name': 'KRW-BTC', 'ma_duration_long': 90, 'ma_duration_mid': 18, 'ma_duration_short': 73, 'ratio_ema_long_rise': 1.0, 'ratio_ema_mid_rise': 1.0004, 'recent_ratio_ema_long_plus': 0.0001, 'successive_rise': 6, 'ratio_ema_mid_long': 0.98, 'diff_vol_aver': 0.5, 'under_long_duration': 17, 'recent_vol_duration': 36, 'sell_method_vol_cri': 0.2, 'ratio_peak_diff': 0.84, 'ratio_open_check': 1.001, 'ratio_reduced': 0.3, 'ratio_mean_long': 0.3, 'continuous_fall': 7, 'continuous_fall_ratio': 0.06, 'ratio_sell_forced': 0.06, 'bought_state': 0, 'bought_price': 0.0}

ETH_1_dic = {'type': 'type_2', 'coin_Name': 'KRW-ETH', 'ma_duration_long': 107, 'ma_duration_mid': 31, 'ma_duration_short': 69, 'ratio_ema_long_rise': 1.0, 'ratio_ema_mid_rise': 1.0003, 'recent_ratio_ema_long_plus': 0.0001, 'successive_rise': 7, 'ratio_ema_mid_long': 0.985, 'diff_vol_aver': 0.3, 'under_long_duration': 17, 'recent_vol_duration': 25, 'sell_method_vol_cri': 0.1, 'ratio_peak_diff': 0.79, 'ratio_open_check': 1.002, 'ratio_reduced': 0.3, 'ratio_mean_long': 0.3, 'continuous_fall': 10, 'continuous_fall_ratio': 0.0, 'ratio_sell_forced': 0.05, 'bought_state': 0, 'bought_price': 0.0}
 
ETC_5_dic = {'type': 'type_2', 'coin_Name': 'KRW-ETC', 'ma_duration_long': 83, 'ma_duration_mid': 24, 'ma_duration_short': 72, 'ratio_ema_long_rise': 1.0, 'ratio_ema_mid_rise': 1.0004, 'recent_ratio_ema_long_plus': 0.0001, 'successive_rise': 6, 'ratio_ema_mid_long': 0.98, 'diff_vol_aver': 0.3, 'under_long_duration': 47, 'recent_vol_duration': 16, 'sell_method_vol_cri': 0.3, 'ratio_peak_diff': 0.87, 'ratio_open_check': 1.0035, 'ratio_reduced': 0.9, 'ratio_mean_long': 0.7, 'continuous_fall': 8, 'continuous_fall_ratio': 0.0, 'ratio_sell_forced': 0.06, 'bought_state': 0, 'bought_price': 0.0}

ARK_14_dic = {'type': 'type_2', 'coin_Name': 'KRW-ARK', 'ma_duration_long': 82, 'ma_duration_mid': 28, 'ma_duration_short': 54, 'ratio_ema_long_rise': 1.0001, 'ratio_ema_mid_rise': 1.0004, 'recent_ratio_ema_long_plus': 0, 'successive_rise': 10, 'ratio_ema_mid_long': 0.98, 'diff_vol_aver': 0.5, 'under_long_duration': 50, 'recent_vol_duration': 19, 'sell_method_vol_cri': 2.5, 'ratio_peak_diff': 0.75, 'ratio_open_check': 1.0029, 'ratio_reduced': 0.5, 'ratio_mean_long': 0.0, 'continuous_fall': 8, 'continuous_fall_ratio': 0.0, 'ratio_sell_forced': 0.09, 'bought_state': 0, 'bought_price': 0.0}

WAXP_57_dic = {'type': 'type_2', 'coin_Name': 'KRW-WAXP', 'ma_duration_long': 102, 'ma_duration_mid': 14, 'ma_duration_short': 71, 'ratio_ema_long_rise': 1.0, 'ratio_ema_mid_rise': 1.0004, 'recent_ratio_ema_long_plus': 0, 'successive_rise': 5, 'ratio_ema_mid_long': 0.985, 'diff_vol_aver': 0.7, 'under_long_duration': 45, 'recent_vol_duration': 14, 'sell_method_vol_cri': 0.1, 'ratio_peak_diff': 0.78, 'ratio_open_check': 1.001, 'ratio_reduced': 0.5, 'ratio_mean_long': 0.1, 'continuous_fall': 3, 'continuous_fall_ratio': 0.03, 'ratio_sell_forced': 0.06, 'bought_state': 0, 'bought_price': 0.0}


# In[4]:


LIST_target = [BTC_0_dic, ETH_1_dic, ETC_5_dic, ARK_14_dic, WAXP_57_dic]


# In[5]:


#LIST_target[0]['coin_Name'][4:]


# In[6]:


len(LIST_target)


# In[7]:


transaction_fee_ratio = 0.0005 + 0.001   # 거래 수수료 비율 + 여유 마진


# In[8]:


#No_of_buyable_items = round(len(LIST_target) * 0.7)   # 동시에 매수 상태일수 있는 최대 종목 수

No_of_buyable_items = 5

print ('No_of_buyable_items :', No_of_buyable_items)


# In[9]:



buyable_budget_ratio = [ ((1 / (No_of_buyable_items - 0)) - transaction_fee_ratio), ((1 / (No_of_buyable_items - 1)) - transaction_fee_ratio), ((1 / (No_of_buyable_items - 2)) - transaction_fee_ratio), ((1 / (No_of_buyable_items - 3)) - transaction_fee_ratio), ((1 / (No_of_buyable_items - 4)) - transaction_fee_ratio)]

'''
buyable_budget_ratio_1 = 0.333 - transaction_fee_ratio - 0.001     # 0.333..  보다 살짝 작은 수치
buyable_budget_ratio_2 = 0.5 - transaction_fee_ratio - 0.001     # 0.5  보다 살짝 작은 수치
buyable_budget_ratio_3 = 1 - transaction_fee_ratio - 0.001     # 1  보다 살짝 작은 수치
'''

time_factor = 9   # 클라우드 서버와 한국과의 시차

check_currency = 'KRW'


# In[10]:


#업비트 계정 설정


# 클라우드용 API 키


access_key = "kuAse9pqZE3mlRJEOanxBXpg8nnPxkw4qf9PI9E8"
secret_key = "rqCdczi9Cvyc9kddASo65RnyGgpPawDEvzj3pn47"



# 집 PC용 API 키
'''
access_key = "RkuEiUN9lvYG5ix2l6ivxBWqYXZ9xleJLkdAJxM4"
secret_key = "JZ4OAGpKivKN9HhfWRZ32q51dGGwnpoCaPn52PYn"
'''

upbit = pyupbit.Upbit(access_key, secret_key)


# In[11]:


candle_type = '60min'
#candle_type = 'day'

if candle_type == '1min' :
    candle_adapt = 'minute1'
    time_unit = 1
elif candle_type == '3min' :
    candle_adapt = 'minute3'
    time_unit = 3
elif candle_type == '5min' :
    candle_adapt = 'minute5'
    time_unit = 5
elif candle_type == '10min' :
    candle_adapt = 'minute10'
    time_unit = 10
elif candle_type == '15min' :
    candle_adapt = 'minute15'
    time_unit = 15
elif candle_type == '30min' :
    candle_adapt = 'minute30'
    time_unit = 30
elif candle_type == '60min' :
    candle_adapt = 'minute60'
    time_unit = 60
elif candle_type == '240min' :
    candle_adapt = 'minute240'
    time_unit = 240
elif candle_type == 'day' :
    candle_adapt = 'day'
    time_unit = (60 * 24)
elif candle_type == 'month' :
    candle_adapt = 'month'
    time_unit = 60 * 24 * 30


# In[12]:


# Test setting
vol_duration = 1 * 365
buy_price_up_unit = 1


# In[13]:



# 코인번호로 코인 명칭 추출
tickers = pyupbit.get_tickers()

LIST_coin_KRW = []

for i in range (0, len(tickers), 1):
    if tickers[i][0:3] == 'KRW':
        LIST_coin_KRW.append(tickers[i])

LIST_check_coin_currency = []

for i in range (0, len(LIST_coin_KRW), 1):
    LIST_check_coin_currency.append(LIST_coin_KRW[i][4:])

LIST_check_coin_currency_2 = []

for i in range (0, len(LIST_check_coin_currency), 1) :
    temp = 'KRW-' + LIST_check_coin_currency[i]
    LIST_check_coin_currency_2.append(temp)


# In[14]:


#LIST_check_coin_currency


# In[15]:


# 매수 최소단위 산출

def unit_value_calc (DF_test) :
    unit_factor = 0
    unit_value = 0
        
    if DF_test['open'][-1] >= 1000000 :  # 200만원 이상은 거래단위가 1000원, 100~200만원은 거래단위가 500원이지만 편의상 200만원 이상과 함께 처리
        unit_factor = -3
        unit_value = 1000
    elif DF_test['open'][-1] >= 100000 :
        unit_factor = -2
        unit_value = 50
    elif DF_test['open'][-1] >= 10000 :
        unit_factor = -1
        unit_value = 10
    elif DF_test['open'][-1] >= 1000 :
        unit_factor = -1
        unit_value = 5
    elif DF_test['open'][-1] >= 100 :
        unit_factor = 0
        unit_value = 1
    else :
        unit_factor = 1
        unit_value = 0.1
    
    print ('DF_test[open][-1] : {0}  /  unit_factor : {1}  /  unit_value : {2}'.format(DF_test['open'][-1], unit_factor, unit_value))
        
    return unit_value


# In[16]:


# 몇건의 과거 이력을 참조할 것인가

candle_count = round((60/time_unit) * 24 * 365 * 5)


# In[17]:


# 잔고 조회, 현재가 조회 함수 정의

def get_balance(target_currency):   # 현급 잔고 조회
    """잔고 조회"""
    balances = upbit.get_balances()   # 통화단위, 잔고 등이 Dictionary 형태로 balance에 저장
    for b in balances:
        if b['currency'] == target_currency:   # 화폐단위('KRW', 'KRW-BTC' 등)에 해당하는 잔고 출력
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_balance_locked(target_currency):   # 거래가 예약되어 있는 잔고 조회
    """잔고 조회"""
    balances = upbit.get_balances()   # 통화단위, 잔고 등이 Dictionary 형태로 balance에 저장
    for b in balances:
        if b['currency'] == target_currency:   # 화폐단위('KRW', 'KRW-BTC' 등)에 해당하는 잔고 출력
            if b['locked'] is not None:
                return float(b['locked'])
            else:
                return 0
    return 0

def get_avg_buy_price(target_currency):   # 거래가 예약되어 있는 잔고 조회
    """평균 매수가 조회"""
    balances = upbit.get_balances()   # 통화단위, 잔고 등이 Dictionary 형태로 balance에 저장
    for b in balances:
        if b['currency'] == target_currency:   # 화폐단위('KRW', 'KRW-BTC' 등)에 해당하는 잔고 출력
            if b['avg_buy_price'] is not None:
                return float(b['avg_buy_price'])
            else:
                return 0
    return 0

'''
def get_current_price(invest_coin):
    """현재가 조회"""
    #return pyupbit.get_orderbook(tickers=invest_coin)[0]["orderbook_units"][0]["ask_price"]
    return pyupbit.get_current_price(invest_coin)
'''
#price = pyupbit.get_current_price("KRW-BTC")


# In[18]:


for i in range (0, len(LIST_target)) :
    if get_balance(LIST_target[i]['coin_Name'][4:]) > 0 :
        LIST_target[i]['bought_state'] = 1
        print ('{0} bought_state is set to {1}'.format(LIST_target[i]['coin_Name'], LIST_target[i]['bought_state']))
    else :
        print ('{0} bought_state is set to {1}'.format(LIST_target[i]['coin_Name'], LIST_target[i]['bought_state']))
    


# In[19]:


#upbit.get_balances()


# In[20]:


# Type_0 방식 매수/매도 함수 정의

def type_0_buy_sell_normal (target_dic) :
    
    print('Under considering')


# In[21]:


# Type_2 방식 매수/매도 함수 정의

def type_2_buy_sell_normal (target_dic) :
    
    #coin_inv = LIST_check_coin_currency_2[target_dic['coin_No']]
    coin_inv = target_dic['coin_Name']
    
    print('\n\ncheck_coin :', coin_inv)
    
    
    # Buy logic 점검
    
    if target_dic['bought_state'] == 0 :   # 매수가 없는 상태라면 
        
        # 전처리
        
        #print ('\nCheking coin is {0}:'.format(coin_inv))
        
        DF_vol_ref = pyupbit.get_ohlcv(coin_inv, count = vol_duration , interval = 'day')
        ref_vol = DF_vol_ref['volume'].sum() / (24 * vol_duration)
        
        DF_test_long = pyupbit.get_ohlcv(coin_inv, count = candle_count, interval = candle_adapt)
        
        DF_test_long['ratio_prior_to_cur'] = DF_test_long['open'] / DF_test_long['open'].shift(1)
        DF_test_long['gap_prior_to_1'] = abs(1 - DF_test_long['ratio_prior_to_cur'])
        
        DF_test_long['fall_check'] = 0
        DF_test_long.loc[(DF_test_long['ratio_prior_to_cur'] <= 1), 'fall_check'] = 1
        
        DF_test_long['ema_long'] = DF_test_long['open'].ewm(span = target_dic['ma_duration_long'], adjust=False).mean()
        DF_test_long['ema_mid'] = DF_test_long['open'].ewm(span = target_dic['ma_duration_mid'], adjust=False).mean()
        DF_test_long['ema_ref'] = DF_test_long['open'].ewm(span = target_dic['ma_duration_short'], adjust=False).mean()

        DF_test_long['ratio_ema_long'] = DF_test_long['ema_long'] / DF_test_long['ema_long'].shift(1)
        DF_test_long['ratio_ema_mid'] = DF_test_long['ema_mid'] / DF_test_long['ema_mid'].shift(1)

        DF_test_long['rise_check_mid'] = 0
        DF_test_long.loc[(DF_test_long['ratio_ema_mid'] > 1), 'rise_check_mid'] = 1

        DF_test_long['ratio_ema_ref'] = DF_test_long['ema_ref'] / DF_test_long['ema_ref'].shift(1)

        DF_test_long['rise_check_ref'] = 0
        DF_test_long.loc[(DF_test_long['ratio_ema_ref'] > 1), 'rise_check_ref'] = 1

        DF_test_long['diff_m_l'] = DF_test_long['ema_mid'] - DF_test_long['ema_long']

        DF_test_long['mid_over_long'] = 0
        DF_test_long.loc[(DF_test_long['diff_m_l'] > 0), 'mid_over_long'] = 1

        DF_test_long['ref_vol_interm'] = DF_test_long['volume'] / DF_test_long.sort_values('volume', ascending=False).tail(round(0.9 * len(DF_test_long)))['volume'].mean()

        DF_test_long['recent_vol_aver'] = 0.0
        for j in range(target_dic['recent_vol_duration'], len(DF_test_long), 1):
            DF_test_long['recent_vol_aver'][j] = DF_test_long.iloc[(j - target_dic['recent_vol_duration']): j]['ref_vol_interm'].sum()
            
        if (DF_test_long['open'][-1] <= 1000) :
            buy_price_up_unit = 1
        elif (1000 < DF_test_long['open'][-1] <= 10000) :
            buy_price_up_unit = 2
        else :
            buy_price_up_unit = 5
        
        investable_budget = 0       
        No_of_bought_items = len(upbit.get_balances())
        
        if (No_of_bought_items <= No_of_buyable_items) and         (DF_test_long['ratio_ema_long'][-3] > target_dic['ratio_ema_long_rise']) and (DF_test_long['ratio_ema_long'][-2] > target_dic['ratio_ema_long_rise']) and         (DF_test_long['ratio_ema_long'][-1] > (target_dic['ratio_ema_long_rise'] + target_dic['recent_ratio_ema_long_plus'])) and (DF_test_long['ratio_ema_mid'][-1] > target_dic['ratio_ema_mid_rise']) and         (DF_test_long.iloc[(-(target_dic['successive_rise'] + 1)) : ]['rise_check_ref'].sum() >= target_dic['successive_rise']) and         ((DF_test_long['ema_mid'][-1] / DF_test_long['ema_long'][-1]) > target_dic['ratio_ema_mid_long']) and         ((DF_test_long.loc[DF_test_long.iloc[-6 : -2]['recent_vol_aver'].idxmax()]['recent_vol_aver'] - DF_test_long['recent_vol_aver'][-2]) < target_dic['diff_vol_aver']) and         (DF_test_long['volume'][-2] >= DF_test_long.iloc[-4 : -2]['volume'].mean()) and         (DF_test_long.iloc[-(target_dic['under_long_duration'] + 1) : -1]['mid_over_long'].sum() == 0) :
            
            if (No_of_bought_items - 1) == 0 :
                investable_budget = get_balance(check_currency) * buyable_budget_ratio[0]
            elif (No_of_bought_items - 1) == 1 :
                investable_budget = get_balance(check_currency) * buyable_budget_ratio[1]
            elif (No_of_bought_items - 1) == 2 :
                investable_budget = get_balance(check_currency) * buyable_budget_ratio[2]
            elif (No_of_bought_items - 1) == 3 :
                investable_budget = get_balance(check_currency) * buyable_budget_ratio[3]
            elif (No_of_bought_items - 1) == 4 :
                investable_budget = get_balance(check_currency) * buyable_budget_ratio[4]            
            
            
            print ('$$$$$ [{0}] buying_transaction is coducting $$$$$'.format(coin_inv))
            
            currrent_price = pyupbit.get_current_price(coin_inv)
            print ('\ncurrent_price : ', currrent_price)
            buyable_price = currrent_price + (buy_price_up_unit * unit_value_calc(DF_test_long))
            buying_volume = investable_budget / buyable_price
            print ('investable_budget : {0} / buyable_price : {1} / buying_volume : {2}'.format(investable_budget, buyable_price, buying_volume))
            
            #transaction_buy = upbit.buy_market_order(coin_inv, investable_budget)   # 시장가로 매수
            transaction_buy1 = upbit.buy_limit_order(coin_inv, buyable_price, buying_volume)   # 지정가로 매수
            time.sleep(30)            
            print ('buy_1ST_transaction_result :', transaction_buy1)
            print ('time : {0}  /  buying_target_volume : {1}  /  bought_volume_until_now : {2}'.format((datetime.datetime.now() + datetime.timedelta(seconds = (time_factor*3600))), buying_volume, get_balance(coin_inv[4:])))
            
            transaction_buy_cancel1 = upbit.cancel_order(transaction_buy1['uuid'])
            
            #target_dic['bought_state'] = 1
            #target_dic['buy_signal_flag'] = 1
            target_dic['bought_time'] = datetime.datetime.now() + datetime.timedelta(seconds = (time_factor * 3600))
    
    
    # 매수상태 점검
        
    if get_balance(coin_inv[4:]) > 0 :
        target_dic['bought_state'] = 1
        print ('bought_state_in mid check : {0}'.format(target_dic['bought_state']))
    else :
        target_dic['bought_state'] = 0
        print ('bought_state_in mid check : {0}'.format(target_dic['bought_state']))
    
    
    # Sell logic
    if target_dic['bought_state'] == 1 :   # 매수가 되어 있는 상태라면
        
        current_time = datetime.datetime.now() + datetime.timedelta(seconds = (time_factor * 3600))
            
        print ('Now : ', current_time)        

        target_coin = target_dic['coin_Name']
                
        time_elapse_bought = math.ceil(((current_time - target_dic['bought_time']).days * 24) + (current_time - target_dic['bought_time']).seconds / 3600)
        print ('time_elapse_bought', time_elapse_bought)
        
        DF_check_sell = pyupbit.get_ohlcv(target_coin, count = round(time_elapse_bought + target_dic['ma_duration_long'] + 1200), interval = candle_adapt)
        
        
        DF_check_sell['ratio_prior_to_cur'] = DF_check_sell['open'] / DF_check_sell['open'].shift(1)
        DF_check_sell['gap_prior_to_1'] = abs(1 - DF_check_sell['ratio_prior_to_cur'])
        
        DF_check_sell['fall_check'] = 0
        DF_check_sell.loc[(DF_check_sell['ratio_prior_to_cur'] <= 1), 'fall_check'] = 1
        
        DF_check_sell['ema_long'] = DF_check_sell['open'].ewm(span = target_dic['ma_duration_long'], adjust=False).mean()
        DF_check_sell['ema_mid'] = DF_check_sell['open'].ewm(span = target_dic['ma_duration_mid'], adjust=False).mean()
        DF_check_sell['ema_ref'] = DF_check_sell['open'].ewm(span = target_dic['ma_duration_short'], adjust=False).mean()

        DF_check_sell['ratio_ema_long'] = DF_check_sell['ema_long'] / DF_check_sell['ema_long'].shift(1)
        DF_check_sell['ratio_ema_mid'] = DF_check_sell['ema_mid'] / DF_check_sell['ema_mid'].shift(1)
        
        
        if (time_elapse_bought > 1) and         (DF_check_sell['volume'][-2] < (target_dic['sell_method_vol_cri'] * DF_check_sell.iloc[-5 : -2]['volume'].mean())) and         ((DF_check_sell['ema_ref'][-1] / DF_check_sell.loc[DF_check_sell.iloc[-(time_elapse_bought + 1) : -1]['high'].idxmax()]['high']) < target_dic['ratio_peak_diff']) :
            
            transaction_sell = upbit.sell_market_order(target_coin, get_balance(target_coin[4:]))  # 시장가에 매도
            time.sleep(5)
            print('\nnow :', (datetime.datetime.now() + datetime.timedelta(seconds=(time_factor * 3600))))
            print('sell_transaction_result_by_ Peak_difference :', transaction_sell)
            
            target_dic['bought_state'] = 0
            target_dic['bought_price'] = 0.0
            target_dic['bought_time'] = 0.0
            
            time.sleep(5)
            
        
        elif (time_elapse_bought > 3) and         (DF_check_sell.iloc[-13 : -1]['open'].std() < (target_dic['ratio_reduced'] * DF_check_sell.iloc[-(time_elapse_bought + 3 + 1) : -(time_elapse_bought - 3 + 1)]['open'].std())) and         (DF_check_sell.iloc[-7: -1]['volume'].mean() < (target_dic['ratio_reduced'] * DF_check_sell.iloc[-(time_elapse_bought + 3 + 1) : -(time_elapse_bought - 3 + 1)]['volume'].mean())) and         (DF_check_sell.loc[DF_check_sell.iloc[-13 : -1]['ratio_prior_to_cur'].idxmax()]['ratio_prior_to_cur'] < target_dic['ratio_open_check']) :
            
            transaction_sell = upbit.sell_market_order(target_coin, get_balance(target_coin[4:]))  # 시장가에 매도
            time.sleep(5)
            print('\nnow :', (datetime.datetime.now() + datetime.timedelta(seconds=(time_factor * 3600))))
            print('sell_transaction_result_by_ Sell_other_way_1 :', transaction_sell)
            
            target_dic['bought_state'] = 0
            target_dic['bought_price'] = 0.0
            target_dic['bought_time'] = 0.0
            
            time.sleep(5)
            
                                      
        elif (time_elapse_bought > 24) and         ((DF_check_sell['ratio_prior_to_cur'][-13 : -1].mean() < 0.995) or          (DF_check_sell.iloc[-25 : -1]['gap_prior_to_1'].mean() < (target_dic['ratio_mean_long'] * (DF_check_sell.iloc[(50 * 24):]['gap_prior_to_1'].mean())))) and         (DF_check_sell.loc[DF_check_sell.iloc[-13 : -1]['ratio_prior_to_cur'].idxmax()]['ratio_prior_to_cur'] < target_dic['ratio_open_check']) :
            
            transaction_sell = upbit.sell_market_order(target_coin, get_balance(target_coin[4:]))  # 시장가에 매도
            time.sleep(5)
            print('\nnow :', (datetime.datetime.now() + datetime.timedelta(seconds=(time_factor * 3600))))
            print('sell_transaction_result_by_ Sell_other_way_2 :', transaction_sell)
            
            target_dic['bought_state'] = 0
            target_dic['bought_price'] = 0.0
            target_dic['bought_time'] = 0.0
            
            time.sleep(5)
        
        
        elif (DF_check_falling.iloc[-(target_dic['continuous_fall'] + 1) : ]['fall_check'].sum() >= target_dic['continuous_fall']) and (DF_check_falling['fall_check'][-1] == 1) and         ((DF_check_falling['open'][-1] / DF_check_falling['open'][-(target_dic['continuous_fall'] + 1)]) < (1 - target_dic['continuous_fall_ratio'])) :
            
            transaction_sell = upbit.sell_market_order(coin_inv_2, get_balance(coin_inv_2[4:]))  # 시장가에 매도
            time.sleep(5)
            print('\nnow :', (datetime.datetime.now() + datetime.timedelta(seconds=(time_factor * 3600))))
            print('sell_transaction_result_by_ Sell other_way_3 (Accumlated falling) :', transaction_sell)
            
            target_dic['bought_state'] = 0
            target_dic['bought_price'] = 0.0
            target_dic['bought_time'] = 0.0
            
            time.sleep(5)
            


# In[ ]:


while True:
    
    try:
        now = datetime.datetime.now() + datetime.timedelta(seconds=(time_factor * 3600))  # 클라우드 서버와 한국과의 시간차이 보정 (9시간)
        print('\n', now)
        
        random_LIST =[]   # 특정 코인에서 에러 발생시 처음부터 Re-try로 인해 타 코인도 점검이 안되는 상황을 최소화 하기 위해, 매 시도마다 순서를 random하게 조정
        
        if (0 < (now.minute % time_unit) <= 9) & (0 < (now.second % 60) <= 59):  # N시:01:00초 ~ N시:05:59초 사이 시각이면
            
            balances = upbit.get_balances()
            print('current_asset_status\n', balances)
            
            random_LIST = random.sample(LIST_target, len(LIST_target))
            
            for i in range(0, len(random_LIST), 1):
                if random_LIST[i]['type'] == 'type_0' :
                    buy_sell_check = type_0_buy_sell_normal (random_LIST[i])
                
                elif random_LIST[i]['type'] == 'type_2' :
                    buy_sell_check = type_2_buy_sell_normal (random_LIST[i])
                
                time.sleep(1)
                
                

        # 손실율이 임계수준을 초과하였을때 강제 매도
        for k in range(0, len(LIST_target), 1):
            coin_inv_2 = LIST_target[k]['coin_Name']
            time.sleep(1)

            if LIST_target[k]['bought_state'] == 1:
                print('[Radical falling] Cheking coin is :', coin_inv_2)
                DF_check_falling = pyupbit.get_ohlcv(coin_inv_2, count = (24 * 10), interval = candle_adapt)
                
                DF_check_falling['ratio_prior_to_cur'] = DF_check_falling['open'] / DF_check_falling['open'].shift(1)
                
                DF_check_falling['fall_check'] = 0
                DF_check_falling.loc[(DF_check_falling['ratio_prior_to_cur'] <= 1), 'fall_check'] = 1
                #print('Cheking radical falling over criteria Loss with coin :', coin_inv_2)
                #print('(pyupbit.get_current_price(coin_inv_2) / get_avg_buy_price(coin_inv_2[4:])) < (1 - LIST_target[k][ratio_sell_forced]) ____ {0} < {1}'.format((pyupbit.get_current_price(coin_inv_2) / get_avg_buy_price(coin_inv_2[4:])), (1 - LIST_target[k]['ratio_sell_forced'])))

                if ((pyupbit.get_current_price(coin_inv_2) / get_avg_buy_price(coin_inv_2[4:])) < (1 - LIST_target[k]['ratio_sell_forced'])):
                    transaction_sell = upbit.sell_market_order(coin_inv_2, get_balance(coin_inv_2[4:]))  # 시장가에 매도
                    time.sleep(5)
                    print('\nnow :', (datetime.datetime.now() + datetime.timedelta(seconds=(time_factor * 3600))))
                    print('sell_transaction_result_by_ radical falling :', transaction_sell)

                    LIST_target[k]['bought_state'] = 0
                    LIST_target[k]['bought_price'] = 0.0
                    LIST_target[k]['bought_time'] = 0.0

                    time.sleep(1)

        time.sleep(10)

    except :
        print ('Error has occured!!!')
        err_msg = traceback.format_exc()
        print(err_msg)
        time.sleep(10)


# In[ ]:




