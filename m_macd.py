import talib
from prettytable import PrettyTable

'''
一个测试与验证MACD在选股与判断大势方面作用的策略。
'''
# this is test by lgy

def initialize(context):
    g.buy_stock_count = 10  # 最大买入股票数
    g.index2 = '000300.XSHG'
    g.index8 = '399006.XSHE'
    g.to_buy_2 = False
    set_benchmark('000300.XSHG')
    set_commission(PerTrade(buy_cost=0.0003, sell_cost=0.0013, min_cost=5))  # 设置手续费率
    set_option('use_real_price', True)


def handle_data(context, data):
    if not [context.current_dt.hour, context.current_dt.minute] == [14, 50]:
        return
    op_buy_stocks = []
    # 20日涨幅
    gr_index2 = get_growth_rate(g.index2)
    gr_index8 = get_growth_rate(g.index8)
    old_to_buy_2 = g.to_buy_2
    g.to_buy_2 = gr_index2 - gr_index8 > 0.08

    if g.to_buy_2:
        record(buy_type=5)
    else:
        record(buy_type=-5)

    # 28转换则清仓重买
    if old_to_buy_2 != g.to_buy_2:
        for stock in context.portfolio.positions.keys():
            order_target(stock, 0)
            log.info("卖出 %s", show_stock(stock))

    # 判断要不要清仓
    if (gr_index2 < 0 and gr_index8 < 0) or (can_sell(g.index2) and can_sell(g.index8)):
        record(buy_type=0)
        for stock in context.portfolio.positions.keys():
            order_target(stock, 0)
            log.info("卖出 %s", show_stock(stock))

    else:
        # 卖出符合条件的股票
        for stock in context.portfolio.positions.keys():
            if can_sell(stock):
                order_target(stock, 0)
                log.info("卖出 %s", show_stock(stock))

        position_count = len(context.portfolio.positions)

        if position_count < g.buy_stock_count:
            # 选取股票，买入
            buy_stocks = get_buy_stocks(context, g.buy_stock_count - position_count)
            if len(buy_stocks) == 0:
                return
            buy_count = 0
            for stock in buy_stocks:
                # 把剩余资金 按待买股数平分
                value = context.portfolio.cash / (len(buy_stocks) - buy_count)
                if context.portfolio.positions[stock].total_amount == 0:
                    log.info("买入 %s", show_stock(stock))
                    op_buy_stocks.append(stock)
                    if order_target_value(stock, value):
                        buy_count += 1
                        if context.portfolio.cash / context.portfolio.total_value < 0.02:
                            break

    # 打印持仓信息
    print
    get_portfolio_info_text(context, op_buy_stocks)
    record(stock_count=len(context.portfolio.positions))


# 判断牛熊分界，当前价格处于250日均线之下时，返回True
def bear_boundary(stock):
    close_data = attribute_history(stock, 250, '1d', ['close'], fq='pre')
    MA250 = close_data['close'].mean()
    cur_price = get_close_price(stock, 1, '1m')
    print
    '判断是否是熊市 : cur_price: %f < MA250: %f ? %s' % (cur_price, MA250, cur_price < MA250)
    return cur_price < MA250


# 选股
def get_buy_stocks(context, count):
    # 根据牛熊市调整不同的PE选股范围
    bear = bear_boundary(g.index2)
    max_pe = 200 if bear else 300

    q = query(valuation.code).filter(
        valuation.pe_ratio > 0,
        valuation.pe_ratio < max_pe
    ).order_by(
        valuation.market_cap.asc()
    ).limit(200)

    df = get_fundamentals(q)
    stock_list = list(df['code'])
    data = get_current_data()
    prices = history(1, unit='1m', field='close', security_list=stock_list)
    # 过滤停牌,ST，涨跌停，已持仓
    stock_list = [stock for stock in stock_list if
                  not data[stock].paused
                  and not data[stock].is_st
                  and prices[stock][-1] < data[stock].high_limit
                  and prices[stock][-1] > data[stock].low_limit
                  and not stock in context.portfolio.positions.keys()
                  ]
    result = []
    result2 = []
    # 优先选取最近三日出现金叉的股票
    for stock in stock_list:
        if can_buy(stock):
            result.append(stock)
            log.info('%s 三日内金叉' % (show_stock(stock)))
            if len(result) >= count:
                break
        elif not can_sell(stock):
            result2.append(stock)

    # 大盘当前价在MA250之上时，以非卖条件补足要购买的股票个数
    if not bear and len(result) < count:
        add_len = count - len(result)
        if len(result2) > add_len:
            result += result2[:count - len(result)]
        else:
            result += result2
    return result

    # # 先获取低位二次金叉的
    # if len(result) < count:
    #     for stock in stock_list:
    #         if can_buy_prior(stock):
    #             result.append(stock)
    #             log.info('%s 低位二次金叉'%(show_stock(stock)))
    #             if len(result) >= count:
    #                 break

    # # 获取最近三天金叉的
    # if len(result) < count:
    #     # # 选股
    #     for stock in stock_list:
    #         if not stock in result and can_buy(stock,3):
    #             result.append(stock)
    #             log.info('%s 三日内金叉'%(show_stock(stock)))
    #             if len(result) >= count:
    #                 break

    # # 获取DIF > DEA 并且非卖条件的
    # if len(result) < count:
    #     for stock in stock_list :
    #         if not stock in result and can_buy_poor(stock):
    #             result.append(stock)
    #             log.info('%s  DIF > DEA '%(show_stock(stock)))
    #             if len(result) >= count:
    #                 break
    # print result
    # return result


'''----------------------------------MACD判断--------------------------'''


# 判断股票是否在买点，看最近三天，是否形成金叉
def can_buy(stock, day_count=3):
    DIF, DEA, macd = MACD(stock)
    for i in range(1, day_count + 1):
        if (DIF[-i] > DEA[-i] and DIF[-i - 1] < DEA[-i - 1]):
            return True
    return False


# 快速线在慢速线之上的
def can_buy_poor(stock):
    DIF, DEA, macd = MACD(stock)
    return (
        DIF[-1] > DEA[-1]
        and DIF[-1] > DIF[-2]  # 判断是否处于上升趋势，实测好像效果不佳
        and DIF[-2] > DIF[-3]
    )


# macd 低位二次金叉选股,有个说法是说能比较大概率出现暴涨，实测意义不大
# 快速慢速线均在低位，并出现两次金叉，并且3日内出现过金叉的。
def can_buy_prior(stock, day_count=3):
    DIF, DEA, macd = MACD(stock)
    count = 0
    for i in range(1, len(macd) - 2):
        if DIF[-i] > 0 or DEA[-i] > 0:
            return False
        if (DIF[-i] - DEA[-i] > 0 and DIF[-i - 1] - DEA[-i - 1] < 0):
            count += 1
            if count >= 2:
                return True
        if i >= day_count and count == 0:
            return False


# 判断股票是否能卖，快速线三天减少，或 死叉
def can_sell(stock, day_count=3):
    DIF, DEA, macd = MACD(stock)
    if DIF[-1] < DEA[-1]:
        return True
    result = True
    for i in range(1, day_count):
        result = result and DIF[-i] < DIF[-i - 1]
    return result


# 获取MACD数据，有增加当日数据
def MACD(stock):
    prices = attribute_history(stock, 130, '1d', ('close'), fq='pre')['close'].values
    # 增加当日数据去计算
    cur_prices = attribute_history(stock, 1, '1m', ('close'), fq='pre')['close'].values
    prices += cur_prices

    DIF, DEA, macd = talib.MACD(prices,
                                fastperiod=12,
                                slowperiod=26,
                                signalperiod=9)
    return DIF, DEA, macd


'''-------------------------------------其它-----------------------------------------'''


# 获取股票n日以来涨幅，根据当前价计算
# n 默认20日
def get_growth_rate(security, n=20):
    lc = get_close_price(security, n)
    c = get_close_price(security, 1, '1m')

    if not isnan(lc) and not isnan(c) and lc != 0:
        return (c - lc) / lc
    else:
        log.error("数据非法, security: %s, %d日收盘价: %f, 当前价: %f" % (security, n, lc, c))
        return 0


# 获取前n个单位时间当时的收盘价
def get_close_price(security, n, unit='1d'):
    return attribute_history(security, n, unit, ('close'), True, fq='pre')['close'][0]


''' ------------------------------获取持仓信息，普通文本格式------------------------------------------'''


def get_portfolio_info_text(context, new_stocks, op_sfs=[0]):
    sub_str = ''
    table = PrettyTable(["仓号", "股票", "持仓", "当前价", "盈亏率", "持仓比"])
    for sf_id in range(len(context.subportfolios)):
        cash = context.subportfolios[sf_id].cash
        p_value = context.subportfolios[sf_id].positions_value
        total_values = p_value + cash
        if sf_id in op_sfs:
            sf_id_str = str(sf_id) + ' *'
        else:
            sf_id_str = str(sf_id)
        for stock in context.subportfolios[sf_id].long_positions.keys():
            position = context.subportfolios[sf_id].long_positions[stock]
            if sf_id in op_sfs and stock in new_stocks:
                stock_str = show_stock(stock) + ' *'
            else:
                stock_str = show_stock(stock)
            stock_raite = (position.total_amount * position.price) / total_values * 100
            table.add_row([sf_id_str,
                           stock_str,
                           position.total_amount,
                           position.price,
                           "%.2f%%" % ((position.price - position.avg_cost) / position.avg_cost * 100),
                           "%.2f%%" % (stock_raite)]
                          )
        if sf_id < len(context.subportfolios) - 1:
            table.add_row(['----', '---------------', '-----', '----', '-----', '-----'])
        sub_str += '[仓号: %d] [总值:%d] [持股数:%d] [仓位:%.2f%%] \n' % (sf_id,
                                                                 total_values,
                                                                 len(context.subportfolios[sf_id].long_positions)
                                                                 , p_value * 100 / (cash + p_value))

    print
    '子仓详情:\n' + sub_str + str(table)



def show_stock(stock):
    return "%s %s" % (stock[:6], get_security_info(stock).display_name)