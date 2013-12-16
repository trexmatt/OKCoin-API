OKCoin-API
==========

This is a simple Python wrapper around the OKCoin.com public and trading API.

It took me quite a while to figure out how to use the API as all the documentation
is in Chinese (and in some cases just bad), so I hope this saves someone some time and frustration.

If this helps you and you'd like to donate, please send coins to

    BTC 19smwQpihXPeXKihG7RxvSvwMoyyggvw3g
    
  
Happy trading :)

Disclaimer
==========

While I've used this code myself and believe it to be error free I cannot guarantee that.  Please read through the code and make changes as you see fit. If you see anything that doesn't seem right, let me know! One important note is that _OKCoin does not use a nonce value_ (an incrementing integer for each trade)!

OKCoin is not affiliated with this project, use at your own risk.

Getting Started
==========

1. The first thing to do is request a partner id and secret key from the OKCoin support on QQ.  You can use QQ if you're not in China.  Support was pretty fast when I did this and it only took ~15 minutes.

2. Next download the okcoin.py file. I haven't included a setup.py as the whole API is quite small.  Only the following standard libraries are needed

    urllib, urllib2, hashlib, simplejson
  
3. Initialize the trade api with your secret key and partner id.  It's probably best to load these from an external file rather than saving them in your trading program.  For getting market data you don't need to do this.

    # Get account balance
  
    import okcoin
  
    partner = your_partner_int_here
    secret_key = your_secret_key_here
  
    T = okcoin.TradeAPI(partner, secret_key)
  
    print( T.getinfo() )
  

  
