OKCoin-API
==========

This is a simple Python wrapper around the OKCoin.com public and trading API.

It took me a while to figure out how to use the API as all the documentation
is in Chinese (and in some cases just bad), so I hope this saves someone some time and frustration.  In case you'd like to write your own code to access the API, I explain how to create the signed string you need for requests in the last section.

If this helps you and you'd like to donate, please send coins to

    BTC 19smwQpihXPeXKihG7RxvSvwMoyyggvw3g
    LTC LfPfo5dn7xSkwrXMgd6ZymPTeQGFJtrcgX
    
Happy trading :)

Disclaimer
==========

While I've used this code myself and believe it to be error free, I cannot guarantee that.  Please read through the code and make changes as you see fit. If you see anything that doesn't seem right, let me know! 

IMPORTANT NOTE: __OKCoin does not use a nonce value!__ This means that if something goes wrong and your program keeps sending the same trade request, OKCoin will keep executing it until you run out of money.  I saw that someone had requested they implement a nonce on the support site so hopefully this happens soon.

OKCoin is not affiliated with this project.  Real trading APIs are included.  Use at your own risk.

Getting Started
==========

1. The first thing to do is request a partner id and secret key from the OKCoin support on QQ.  You can use QQ if you're not in China.  Support was pretty fast when I did this and it only took ~15 minutes.

2. Next download the okcoin.py file. I haven't included a setup.py as the whole API is quite small.  Only the following standard libraries are needed

        urllib, urllib2, hashlib, simplejson
  
3. Initialize the trade api with your secret key and partner id.  It's probably best to load these from an external file rather than saving them in your trading program.  For getting market data you don't need to do this.

        # Get account balance
  
        import okcoin
  
        partner = your_partner_int_here
        secret_key = your_secret_key_str__here
  
        T = okcoin.TradeAPI(partner, secret_key)
  
        print( T.getinfo() )
  

Request Structure
==========

If you're using the okcoin.py file as is, ignore this section.

If you'd like to write your own code for the API, I explain the request structure below.  This took a while to figure out as the documentation on the OKCoin website is quite lacking (and Google Translate probably didn't help :D ).

1. Take the list of parameters and values you're requesting, sort it alphabetically and then join each with "&"
Note that all parameter names must be __lowercase__ and have __no spaces__.  The example they show is on the page (http://www.okcoin.com/t-1000097.html) is actually incorrect because of this.

        e.g. "amount=1.0&partner=2088101568338364&rate=680&symbol=btc_cny&type=buy"

2. Take the string you made above and add your secret key to the end of it with __no spaces__ OR __"&"__

        e.g. "amount=1.0&partner=2088101568338364&rate=680&symbol=btc_cny&type=buy111111111111111111111111"
    
3. MD5 hash that string, convert it to hex, make it uppercase then URL encode it and POST to the relevant page (depending on what request you're making).


        # Calculating signed string to get account balance
    
        import urllib
        import urllib2
        import hashlib
        import simplejson
        
        # partner is int
        # secret_key is string
     
        partner = 1111111111
        secret_key = 'THISISNOTANACTUALKEYOBVIOUSLY'
         
        user_info_url = 'https://www.okcoin.com/api/userinfo.do'
        sign_string = 'partner=' + str(partner)
         
        m = hashlib.md5()
        m.update(sign_string + secret_key)
        signed = m.hexdigest().upper()
         
        values = {'partner' : partner,
                  'sign' : signed}
         
        data = urllib.urlencode(values)
        req = urllib2.Request(user_info_url, data)
        response = urllib2.urlopen(req)
        result = simplejson.load(response)
         
        print( result['info']['funds']['free'] )
    
    




