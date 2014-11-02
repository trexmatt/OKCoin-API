import requests
import hashlib
import simplejson

class TickerObject(object):

    def __init__(self,data):
        self.bid = data['ticker']['buy']
        self.ask = data['ticker']['sell']
        if( 'high' in data ):
            self.high = data['ticker']['high']
            self.low = data['ticker']['low']
            self.last = data['ticker']['last']
            self.volume = data['ticker']['volume']

class DepthObject(object):

    def __init__(self,data):
        self.asks = {}
        for l in data['asks']:
            self.asks[l[0]] = l[1]
        self.bids = {}
        for l in data['bids']:
            self.bids[l[0]] = l[1]   
    
class MarketData(object):

    def __init__(self):
        self.http = requests.Session()

    def get_json(self, url):
        r = self.http.get(url)
        data = simplejson.loads(r.content)
        return(data)
        
    def ticker(self, symbol):
        btc_ticker_url = 'https://www.okcoin.com/api/ticker.do?symbol=btc_cny'
        ltc_ticker_url = 'https://www.okcoin.com/api/ticker.do?symbol=ltc_cny'
        if( symbol == 'btc_cny' ):
            data = self.get_json(btc_ticker_url)
            return( TickerObject(data) )
        if( symbol == 'ltc_cny' ):
            data = self.get_json(ltc_ticker_url)
            return( TickerObject(data) )
        if( symbol == 'ltc_btc' ):
            btc_data = self.get_json(btc_ticker_url)
            ltc_data = self.get_json(ltc_ticker_url)
            ltc_btc_bid = round( float(ltc_data['ticker']['buy']) / float(btc_data['ticker']['sell']), 8 )
            ltc_btc_ask = round( float(ltc_data['ticker']['sell']) / float(btc_data['ticker']['buy']), 8 )
            data = { 'ticker' : {"sell" : ltc_btc_ask, "buy" : ltc_btc_bid} }
            return( TickerObject(data) )
        else:
            print('Unrecognized symbol: ' + symbol)

    def get_depth(self, symbol):
        btc_depth_url = 'https://www.okcoin.com/api/depth.do?symbol=btc_cny'
        ltc_depth_url = 'https://www.okcoin.com/api/depth.do?symbol=ltc_cny'
        if( symbol == 'btc_cny' ):
            data = self.get_json(btc_depth_url)
            return( DepthObject(data) )
        if( symbol == 'ltc_cny' ):
            data = self.get_json(ltc_depth_url)
            return( DepthObject(data) )
        else:
            print('Unrecognized symbol: ' + symbol)

    def get_history(self, symbol):
        btc_history_url = 'https://www.okcoin.com/api/trades.do?symbol=btc_cny'
        ltc_history_url = 'https://www.okcoin.com/api/trades.do?symbol=ltc_cny'
        if( symbol == 'btc_cny' ):
            return( self.get_json(btc_history_url) )
        if( symbol == 'ltc_cny' ):
            return( self.get_json(ltc_history_url) )
        else:
            print('Unrecognized symbol: ' + symbol)

    def future_ticker(self,symbol, contract):
        url = 'https://www.okcoin.com/api/future_ticker.do?symbol='+symbol+'&contractType='+contract
        return self.get_json(url)

class TradeAPI(MarketData):
    
    def __init__(self, partner, secret):
        MarketData.__init__(self)
        self.partner = partner
        self.secret = secret

        # partner is integer, secret is string

    def _post(self, params, url):

        # params does not include the signed part, we add that

        sign_string = ''
        
        for pos,key in enumerate(sorted(params.keys())):
            sign_string += key + '=' + str(params[key])
            if( pos != len(params) - 1 ):
                sign_string += '&'
                
        sign_string += self.secret
        m = hashlib.md5()
        m.update(sign_string)
        signed = m.hexdigest().upper()

        params['sign'] = signed

        req = self.http.post(url,params=params)
        result = simplejson.loads(req.content)

        success = result[u'result']
        if( not success ):
            print('Error: ' + str(result[u'errorCode']))
            print( self.error_code_meaning(result[u'errorCode']) )
            return(result)
        else:
            return(result)

    def get_info(self):
        params = {'partner' : self.partner}
        user_info_url = 'https://www.okcoin.com/api/userinfo.do'
        return(self._post(params, user_info_url))

    def trade(self, symbol, trade_type, rate, amount):
        params = { 'partner' : self.partner,
                   'symbol' : symbol,
                   'type' : trade_type,
                   'rate' : rate,
                   'amount' : amount }
        trade_url = 'https://www.okcoin.com/api/trade.do'
        return(self._post(params, trade_url))

    def cancel_order(self, order_id, symbol):
        params = { 'partner' : self.partner,
                   'order_id' : order_id,
                   'symbol' : symbol }
        cancel_order_url = 'https://www.okcoin.com/api/cancelorder.do'
        return(self._post(params, cancel_order_url))

    def get_order(self, order_id, symbol):
        params = { 'partner' : self.partner,
                   'order_id' : order_id,
                   'symbol' : symbol }
        get_order_url = 'https://www.okcoin.com/api/getorder.do'
        return(self._post(params, get_order_url))

    def error_code_meaning(self, error_code):
        codes = { 10000 : 'Required parameter can not be null',
                  10001 : 'Requests are too frequent',
                  10002 : 'System Error',
                  10003 : 'Restricted list request, please try again later',
                  10004 : 'IP restriction',
                  10005 : 'Key does not exist',
                  10006 : 'User does not exist',
                  10007 : 'Signatures do not match',
                  10008 : 'Illegal parameter',
                  10009 : 'Order does not exist',
                  10010 : 'Insufficient balance',
                  10011 : 'Order is less than minimum trade amount',
                  10012 : 'Unsupported symbol (not btc_cny or ltc_cny)',
                  10013 : 'This interface only accepts https requests' }
        return( codes[error_code] )
                   
    def get_future_info(self):
        params = {'partner' : self.partner}
        user_info_url = ' https://www.okcoin.com/api/future_userinfo.do'
        return(self._post(params, user_info_url))

    def get_future_holdings(self, symbol):
        params = {'partner' : self.partner,
            'symbol': symbol}
        holdings_url = 'https://www.okcoin.com/api/future_position.do'
        return(self._post(params, holdings_url))

    def future_trade(self, symbol, contract, price, amount, type):
        params = {'partner' : self.partner,
            'symbol': symbol,
            'contractType': contract,
            'price':price,
            'amount': amount,
            'type':type,
            'matchPrice':0}
        url = 'https://www.okcoin.com/api/future_trade.do'
        return(self._post(params, url))
                   
