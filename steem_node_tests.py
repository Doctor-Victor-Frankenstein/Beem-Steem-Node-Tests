import datetime, csv, os

from beem import Steem, blockchain
from beem.account import Account
from beem.comment import Comment
from beem.nodelist import NodeList

# exports list to csv file
def export_csv(name,input_list):
    cwd = os.getcwd()
    filename=datetime.datetime.now().strftime(name+"%Y%m%d-%H%M%S.csv")
    keys = input_list[0].keys()
    outfile=open(cwd+'/'+filename,'w')
    writer=csv.DictWriter(outfile, keys)
    writer.writeheader()
    writer.writerows(input_list)

status = []

# obtains current Beem nodes
nodes = NodeList().get_nodes()

for n in nodes:
    Connectivity = {}
    Configuration = {}
    Streamable = {}
    Account_Class = {}
    Comment_Class = {}
    try:# simple connection test
        stm = Steem(node=n,num_retries=1,num_retries_call=1)
        print("Successfully connected to "+n)
        Connectivity = {'Connectivity': True, 'Error': 'n/a'}
    except Exception as e:
        Connectivity = {'Connectivity': False, 'Error': e}
        print("Connection error on "+n)
        status.append({'Node':n,'Connectivity': 'No','Configuration':'n/a','Account':'n/a','Comment':'n/a'})
        continue
    try:# obtain node config test
        stm.get_config()
        print("Obtained config from node "+n)
        Configuration = {'Get_Config':'Success', 'Error': 'n/a'}
    except Exception as e:
        Configuration = {'Get_Config':'Failure', 'Error': e}
        Configuration = False
    try:# obtain account test
        a = Account('anthonyadavisii',steem_instance=stm)
        print("Obtained account information")
        Account_Class = {'Account_Class':'Success', 'Error': 'n/a'}
    except Exception as e:
        print("Failed to obtain account information")
        Account_Class = {'Account_Class':'Failure', 'Error': e}
    try:# obtain comment test
        c = Comment('@anthonyadavisii/sfr-bot-troubleshooting-session-1-node-issues-beem-python',steem_instance=stm)
        print("Obtained comment information for "+c.author+"'s post")
        Comment_Class = {'Comment_Class':'Success', 'Error': 'n/a'}
    except Exception as e:
        print("Failed to obtain comment and/or metadata")
        Comment_Class = {'Comment_Class':'Failure', 'Error': e}
    try:# blockchain stream test
        for op in blockchain.Blockchain(steem_instance=stm).stream():
            print(op)
            Streamable = {'Stream Chain': 'Success', 'Error': 'n/a'}
            break
    except Exception as e:
        print("Failed to stream blockchain")
        Streamable = {'Stream Chain': 'Failure', 'Error': e}
    status.append({'Node':n,'Connectivity': Connectivity,'Configuration':Configuration,'Account':Account_Class,'Comment':Comment_Class,'Stream Chain': Streamable})

export_csv('nodestatus',status)