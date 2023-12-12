# https://www.askpython.com/python-modules/ipaddress-module

import ipaddress

#ipn= ipaddress.ip_network('1.0.0.0/24')
#print(list(ipn.hosts()))

# subnetting

#ipn1 = ipaddress.ip_network("1.0.0.0/24")

#default prefixlen_diff=1 ?
#print(list(ipn1.subnets()))

#prefixlen_diff is the amount pf prefix length that should be increased 
#print(list(ipn1.subnets(prefixlen_diff=1)))
#new_prefix is the new prefix of the subnets and is larger than our prefix  : 25 = 24 + 1
#print(list(ipn1.subnets(new_prefix=25)))

import sys

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

import os
import pickle

# future config ...
#from django.conf import settings
#HOME = settings.BASE_DIR

def storeDatadb(db,dbname):

    #storefilepath = os.path.join(HOME, "app", "tools", dbname)
    storefilepath = os.path.join(dbname)

    # Its important to use binary mode
    dbfile = open(storefilepath, 'wb')

    # source, destination
    pickle.dump(db, dbfile)
    dbfile.close()

def loadData(dbname):

    #storefilepath = os.path.join(HOME, "app", "tools", dbname)
    storefilepath = os.path.join(dbname)

    # for reading also binary mode is important
    dbfile = open(storefilepath, 'rb')
    db = pickle.load(dbfile)

    #for keys in db:
    #    print(keys, '=>', db[keys])

    dbfile.close()

    return db

class Subnets:
    def __init__(self,net=""):
        
        # load stored data       
        if net == "":
            ret = loadData("network.pic")
            if ret != []:
                self.rootNetItem = ret
            else:
                print("Input network. No stored data")    
                sys.exit()
        else:
            # erase stored data
            storeDatadb([],"network.pic")
            #                  netip,subnets,info used net,level,nrcrt subnetization,nrcrt select usable net
            #                        children
            self.rootNetItem = [ipaddress.ip_network(net),[],"",0,0,0]
        
        # self.rootNet = net
               
        self.nrcrt = 0
        
        self.parent = None

    def reset():
            # erase stored data
            storeDatadb([],"network.pic")        

    def scan_tree(self,netItem,param,param2,param3):
        pass
        net = netItem[0]
        subnets = netItem[1]
        info = netItem[2]
        level = netItem[3]
        nrcrt_subnet_op = netItem[4]
        nrcrt_usable_op = netItem[5]

        self.parent = None

        if param == "lastop":
            pass
            if nrcrt_subnet_op > self.maxop:
                self.maxop = nrcrt_subnet_op
                self.op = "subnet" 
            if nrcrt_usable_op > self.maxop:
                self.maxop = nrcrt_usable_op
                self.op = "usable" 
                
        if param == "back":
            pass
            #print("recursive back last op",nrcrt_subnet_op,nrcrt_usable_op,self.maxop,self.op)
            
            if self.op == "subnet" and nrcrt_subnet_op == self.maxop:
                pass
                #print("?",self.lastparent)
                print("mark subnet for delete",netItem)    
                
                self.parent = self.lastparent
                
                #parentSubnets = self.lastparent[1]
                # this stops recursivity !
                #parentSubnets.remove(netItem)
                                
                # so just mark ncrcrt op with -1 for delete afterwards, below
                netItem[4] = -1
                
            if self.op == "usable" and nrcrt_usable_op == self.maxop:
                                
                # unmark the info
                netItem[2] = ""
                # none op nrcrt
                netItem[5] = 0
                
                return

        if subnets != []:
            # is subnetted
            color = bcolors.FAIL
        else:
            # is not ...
            color = bcolors.OKBLUE

        if param == "available":
            
            hosts = net.hosts()
            broadcast = net.broadcast_address
       
            all = []
            for host in hosts:
                all.append(host)
            
            start = all[0]
            end = all[-1]
            
            #print(f"{color} {' '*level} -{level} {net} - {broadcast} {info} [{nrcrt_subnet_op}] [{nrcrt_usable_op}] {bcolors.ENDC}")        
            print(f"{color} {' '*level} -{level} {net} - {broadcast} {info}  [{start}-{end}] {bcolors.ENDC}")        

        # available nets for choosing subnet/usage
        if subnets == []:
            # and not marked with info != "" means available nets for subnetting or usage
            if info == "":
                self.results.append(netItem)

        # memorize parent for removing children in "back" option
        if subnets != []:
            self.lastparent = netItem

        for netItem in subnets:                        
            self.scan_tree(netItem,param,param2,param3)
            
   

    def walk_tree(self,param="",param2="",param3=""):
        self.level = 0
        self.results = []
        # recursive scan tree
        #print(">>>>>>>>>>>>>>>")
        self.scan_tree(self.rootNetItem,param,param2,param3)
        #print("<<<<<<<<<<<<<<<")

    def subnets(self,netItem,prefix,info=""):
        self.nrcrt += 1
    
        net = netItem[0]
        level = netItem[3]
        subnets_list = list(net.subnets(new_prefix=prefix))
        #print(subnets_list)

        for subnet in subnets_list:
            newNetItem = [subnet,[],info,level+1,self.nrcrt,0]
            netItem[1].append(newNetItem)

        storeDatadb(self.rootNetItem,"network.pic")    

    def mark(self,netItem,info=""):
        self.nrcrt += 1
        
        netItem[2] = info
        netItem[5] = self.nrcrt
        
        storeDatadb(self.rootNetItem,"network.pic")    

    def available(self):

        self.walk_tree("available")

        print("available nets")
        n = 0
        for netItem in self.results:
            if (netItem[2] == ""):
                print(f"{n}: {netItem[0]}")
                n+=1
    
    # back operation                            
    def back(self):
        pass
    
        self.maxop = 0
        self.op = ""
        #identify last op (max op number)
        self.walk_tree("lastop")
        print("remove last op",self.maxop,self.op)
        #unmark used net or delete subnets
        self.walk_tree("back")
        
        if self.parent:
            
            subnets = self.parent[1]
            
            # for subnet in subnets:
            #     if subnet[4] == -1:
            #         print("delete subnet",subnet,self.lastparent)
            #         subnets.remove(subnet)
            # print(self.parent)        
            
            # remove subnets marked above with -1 at nrcrt op    
            newlist = [subnet for subnet in subnets if subnet[4] != -1] 

            self.parent[1] = newlist
            
        storeDatadb(self.rootNetItem,"network.pic")    

    def testn(self,number):
        try:
            n = int(number)
            return n
        except Exception as e:
            print(f"{e}")    
            sys.exit() 
        
    # choose network for subneting    
    def operation_subnet(self,param):
        pass
        items = param.split("/")
        index = items[0]
        index = self.testn(index)
        bits = items[1]
        bits = self.testn(bits)

        netItem = self.results[index]    
        self.subnets(netItem,bits)        
        
    # choose network for usage
    def operation_mark_used(self,param):
        pass
        items = param.split("/")
        index = items[0]
        index = self.testn(index)
        info = items[1]
        
        netItem = self.results[index]
        self.mark(netItem,info)
        


help = '''
Input 0 (load stored data)  or 1 (network) parameters
'''
options ='''
Choose options:
s - subnetting
u - used net
b - back/reverse last operation
'''

                       
    

if __name__ == "__main__":
    pass

    #print (f'Number of arguments:  {len(sys.argv)}')
    #print (f'Argument List: {str(sys.argv)}')

    if len(sys.argv) == 1:
        #s = Subnets("")
        net = ""
        
    elif len(sys.argv) == 2:
        
        if(sys.argv[1] == "-h"):
            print(help)   
            sys.exit() 
    
        net = sys.argv[1]
        try:
            testnet = ipaddress.ip_network(net)
        except Exception as e:
            print(f"{e}")    
            sys.exit()

    else:
        print("Input 0 parameters (load stored data)  or 1 parameter (network)")
        sys.exit()

            
    s = Subnets(net)
    
    while True:
        s.available()   
        key = input(options)
        
        if key == "s":
            pass
        
            arg = input("Choose network index/networkbits: ")                
            s.operation_subnet(arg)
                    
        elif key == "u":
            pass
            
            arg = input("Choose network index/description(info of used net): ")
            s.operation_mark_used(arg)

        elif key == "b":
            pass
        
            s.back()
            
        #     elif key == "3":
        #         print("3")    
        else:
            print("undefined option")            

    


    # if len(sys.argv) != 2:
    #     print("Input network or ")
    # else:    
    #     net = sys.argv[1]
    #     #ipaddress.ip_network(net)
    #     s = Subnets(net)
        





    #s = Subnets("1.0.0.0/24")

    # # -----------------------------------------
    # s.available()
    # # choose root network for subnetting
    # netItem = s.results[0]
    # # subnetting with 25 bits network portion
    # s.subnets(netItem,25)
    # # -----------------------------------------

    # # -----------------------------------------
    # s.available()
    # # choose network for usage
    # netItem = s.results[0]
    # s.mark(netItem,"for 100 hosts")

    # # choose network for subneting
    # netItem = s.results[1]    
    # s.subnets(netItem,26)
    # # ----------------------------------------
    
    # # ----------------------------------------
    # s.available()
    # # choose network for usage
    # netItem = s.results[0]
    # s.mark(netItem,"for 50 hosts")

    # # choose network for subnetting
    # netItem = s.results[1]
    # s.subnets(netItem,27)
    # # ---------------------------------------
        
    # # ---------------------------------------
    # s.available()
    # # choose network for usage
    # netItem = s.results[0]
    # s.mark(netItem,"for 20 hosts")

    # # choose network for subnetting
    # netItem = s.results[1]
    # s.subnets(netItem,28)
    # # --------------------------------------


    # # ---------------------------------------
    # s.available()
    # # choose network for usage
    # netItem = s.results[0]
    # s.mark(netItem,"for 10 hosts")

    # # choose network for subnetting
    # netItem = s.results[1]
    # s.subnets(netItem,29)
    # # --------------------------------------

    # # ---------------------------------------
    # s.available()
    # # choose network for usage
    # netItem = s.results[0]
    # s.mark(netItem,"for 6 hosts")

    # # choose network for subnetting
    # netItem = s.results[1]
    # s.subnets(netItem,30)
    # # --------------------------------------

    # # ---------------------------------------
    # s.available()
    # # choose network for usage
    # netItem = s.results[0]
    # s.mark(netItem,"for 2 hosts")

    # # choose network for usage
    # netItem = s.results[1]
    # s.mark(netItem,"for 2 hosts")
    # # ---------------------------------------

    # s.available()

    #print(s.rootNetItem)

    # baack de completat

    # 3/4 options: subnet/usage/supernet? (info) or back
    
    # avalable+options+available+options ...

    
    # ==========================================
    # test pickle store temporary data     
    # # initializing data to be stored in db
    # Omkar = {'key' : 'Omkar', 'name' : 'Omkar Pathak',
    # 'age' : 21, 'pay' : 40000}
    # Jagdish = {'key' : 'Jagdish', 'name' : 'Jagdish Pathak',
    # 'age' : 50, 'pay' : 50000}

    # # # database
    # db = {}
    # db['Omkar'] = Omkar
    # db['Jagdish'] = Jagdish

    # storeDatadb(db,"access_token.pic")
    # ret = loadData("access_token.pic")
    # print(ret)
    # ===========================================
    