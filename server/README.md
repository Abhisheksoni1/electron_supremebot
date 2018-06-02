++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Manual Captcha Harvester

## IMPORTANT NOTE
This will NOT work on supreme. This is because supreme check the domain the captcha is solved on. Using this
harvesting method, all captchas are harvested on cartchefs.supremenewyork.com instead of supremenewyork.com
so supreme will give you a checkout error when using those tokens. The alternative is to set this harvester
up on another server, change the hosts file of that server to be `127.0.0.1 supremenewyork.com` and use
something like nginx or ngrok to make the `/token` endpoint externally accessible. If you try change the host
file to `127.0.0.1 supremenewyork.com` on the same PC your supreme bot is running on, your cart/checkout requests
will go to your localhost IP, not the supreme servers. The other alternative is to use a chrome extension to
harvest (like BNB do) or to create some kinda of standalone harvester (like OSS or slayer).

## Description
This simple script allows the user to manually harvest captchas and request them from the local server when needed.
The token management is handled entirely by the server.

## Requirements
  - Python 3+
  The following modules must also be installed and can be with pip e.g. `pip install colorama`
  - `colorama`
  - `termcolor`
  - `flask`
  
## Instructions
  - The most important step is to know how to edit your hosts file. You can find out how to do this with a simple
  google search. You will need to add an entry to your hosts file like so `127.0.0.1 cartchefs.DOMAIN-HERE` -
  replacing DOMAIN-HERE with the domain you are harvesting for e.g. supremenewyork.com or adidas.com or sneakersnstuff.com
  - Open config.json in an editor such as atom or sublime and make the necessary changes to the file. Making sure the
  domain is entered without the `www` and the sitekey is correct and the latest one available
  - cd into the directory of the repository
  - `python main.py` to run the script
  
  To request tokens from the server, you must send a GET request to `http://cartchefs.DOMAIN-HERE:5000/token`.
  The token that is set to expire next will be returned in text format. It is advised to only request tokens from the
  server right when you are about to use them.
  The alternative is to call the `sendToken` function from your own script
  
## FAQ
  - The captcha solving page will not load... *attempt to reload it manually and check you edited your hosts file correctly*
  - Can you help me... *yeah I probably could but I likely won't so try work out your own issues xox*
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


how to start captcha server

python manage.py start_harvester

and it work like charm :D
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
]



