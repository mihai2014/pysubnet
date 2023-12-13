    # Python script for subnetting IPv4 networks

Modules needed:

```
pip install ipaddress
```

Usage: 

```
python subnets.py -h 
```
    
for help

Start computing with root network as parameter:

```
python subnets.py 172.16.0.0/23
```

then, after eventual stoping of script, reload script without parameters for continuing calculations 

```
python subnets.py 172.16.0.0/23
```

Defined network configurations are stored in network.pic file

### Reference docs:

https://docs.python.org/3/library/ipaddress.html

https://docs.python.org/3/howto/ipaddress.html

https://www.askpython.com/python-modules/ipaddress-module

