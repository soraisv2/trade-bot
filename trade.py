#!/usr/bin/env python3
##
## EPITECH PROJECT, 2021
## Project
## File description:
## trade.py
##

import csv

def load_data(filename):
    data = []
    with open(filename, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        next(reader)
        for row in reader:
            data.append(row)
        return (data)

def get_stdin():
    cmd = input("Command:\n")
    return cmd

def getData(update):
    update = update.split(',')
    for item in update:
        item = item.split(":")
        currency = item[0]
        item.pop(0)
        stack[currency] = item[0]

wallet = {'USDT': {'total': 1000.0}, 'BTC': { 'total' : 0, 'actions' : [] }, 'ETH': { 'total' : 0, 'actions' : [] }}
next_candles = {
    'BTC_ETH': {'date': [], 'high': [], 'low': [], 'open':[], 'close':[], 'volume':[]},
    'USDT_ETH': {'date': [], 'high': [], 'low': [], 'open':[], 'close':[], 'volume':[]},
    'USDT_BTC': {'date': [], 'high': [], 'low': [], 'open':[], 'close':[], 'volume':[]}
}
statistic = {
    'moyenne': {
        'BTC_ETH': {'high': [], 'low': [], 'open':[], 'close':[], 'volume':[]},
        'USDT_ETH': {'high': [], 'low': [], 'open':[], 'close':[], 'volume':[]},
        'USDT_BTC': {'high': [], 'low': [], 'open':[], 'close':[], 'volume':[]}
    },
    'ratio': {
        'BTC_ETH': {'high': [], 'low': [], 'open':[], 'close':[], 'volume':[]},
        'USDT_ETH': {'high': [], 'low': [], 'open':[], 'close':[], 'volume':[]},
        'USDT_BTC': {'high': [], 'low': [], 'open':[], 'close':[], 'volume':[]}
    }
}
update = {}
stack = {}
action = {}
period = 10

def estimation():
    currency = ['BTC_ETH', 'USDT_ETH', 'USDT_BTC']
    datas = ['high', 'low', 'open', 'close', 'volume']
    for cur in currency:
        for data in datas:
            if (len(next_candles[cur][data]) >= period):
                ratio = (float(next_candles[cur][data][-1]) - float(next_candles[cur][data][-period])) / float(next_candles[cur][data][-period])
                statistic['ratio'][cur][data].append(ratio * 100)
    for cur in currency:
        for data in datas:
            if (len(next_candles[cur][data]) >= period):
                moy = 0
                for value in next_candles[cur][data][-period:]:
                    moy += float(value)
                statistic['moyenne'][cur][data].append(moy / period)

def updateData(update):
    update = update.split(";")
    for item in update:
        item = item.split(",")
        currency = item[0]
        item.pop(0)
        next_candles[currency]['date'].append(item[0])
        next_candles[currency]['high'].append(item[1])
        next_candles[currency]['low'].append(item[2])
        next_candles[currency]['open'].append(item[3])
        next_candles[currency]['close'].append(item[4])
        next_candles[currency]['volume'].append(item[5])
    estimation()

def trade():
    if (wallet['ETH']['total'] != 0):
        i = 0
        selling = 0
        while (i < len(wallet['ETH']['actions'])):
            if (float(update['next_candles']['USDT_ETH']['high'][-1]) > 1):
                if (float(update['next_candles']['USDT_ETH']['close'][-1]) > wallet['ETH']['actions'][i]['price'] + 500):
                    selling += wallet['ETH']['actions'][i]['quantity']
                    wallet['ETH']['total'] -= wallet['ETH']['actions'][i]['quantity']
                    del wallet['ETH']['actions'][i]
            i += 1
        if (selling != 0):
            print("sell USDT_ETH " + str(selling))
            wallet['USDT']['total'] += selling * float(update['next_candles']['USDT_ETH']['close'][-1])
            return
    else:
        i = 1
        while (i < 6):
            if (statistic['ratio']['USDT_ETH']['high'][-i] > -1):
                break
            i += 1
        if (i == 6):
            achat = wallet['USDT']['total'] / 2
            price = float(update['next_candles']['USDT_ETH']['close'][-1])
            quant = achat / price
            print("buy USDT_ETH " + str(quant))
            wallet['ETH']['actions'].append({
                'price': price,
                'quantity': quant
                })
            wallet['ETH']['total'] += quant
            wallet['USDT']['total'] -= achat
            return
    print ("pass")

def main():
    while 1:
        line = input()
        line = line.split()
        if line[0] == "action" and line[1] == "order":
            trade()
        elif line[0] == "update":
            if line[2] == "next_candles":
                updateData(line[3])
                update[line[2]] = next_candles
            elif line[2] == "stacks":
                getData(line[3])
main()