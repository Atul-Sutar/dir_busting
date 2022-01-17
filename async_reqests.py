'''
Directory Busting Tool

This script bust the directories against website.
this usge asyncronous approach while busting directories

Athor : Atul S.'''

from tqdm import tqdm
import requests
import asyncio
import aiohttp
import socket
import time
import sys

# checking arguments
if len(sys.argv) != 3:
    print('''
Usage:    python3 {} https://target.com /wordlist_path
Example:  python3 pybuster.py https://my-website.com /directory_list.txt 
    '''.format(sys.argv[0]))
    sys.exit()

# checing host directory
if str(sys.argv[1])[-1] != '/':
    url = str(sys.argv[1])+str('/')+'{}'
else:
    url = str(sys.argv[1])+'{}'
'''
# checking Connection
print(f"[+] Target Website Set To {url.replace('{}','')}")
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
    global HOST, PORT
    if 'https://' in sys.argv[1]:
        HOST = socket.gethostbyname(str(sys.argv[1].replace('https://',"")).replace('/',""))
        PORT = 80
    elif 'http://' in sys.argv[1]:
        HOST = socket.gethostbyname(str(sys.argv[1].replace('http://',"")).replace('/',""))
        PORT = 80 
except socket.gaierror:
    print("DNS cound not be resolved")
    s.close()
    sys.exit()
except socket.error:
    print("cannot connect to host")
    s.close()
    sys.exit()
    
print("[+] Checking Target Connection")
r = s.connect_ex((str(HOST),PORT))
if r == 0:
   print("[+] Target Is Available")
   s.close()
else:
    print(f"[-] Unable to Connect {sys.argv[1]}")
    print("Please check Connection And Try Again")
    sys.exit()

s.close()'''
# checking wordlist
print(f"[+] Opening Directory List From {sys.argv[2]}")

try:
    with open(str(sys.argv[2]),'r') as f :
        directories = [d.replace('\n','') for d in f.readlines()]
except:
    print("[-] Cannot Open Specified Word List")
    print("Please Provide Full Path or Name Only If It In Current Directory")
    sys.exit()

print("[+] We Have Wordlist of",len(directories))
#print('\n')

# main Programme
result = []
tasks = []

def main():

    # Creating session and appends to list 
    def tasks_create(session):
        print("[+] Making Request")
        for directory in tqdm(directories):
            #print(f'Trying --> {directory}',end="\r",flush=True)
            tasks.append({'url' : session.get(url.format(directory.strip()),ssl=False),'dir': directory})
        #print('\n')
        return tasks
         
    # Creating Session and Passing to Create task retrns tasks and run with async gather. append result
    async def get_session():
        try:
            async with aiohttp.ClientSession() as session:
                task = tasks_create(session)
                responces = await asyncio.gather(*list(task['url'] for task in tasks))
                print('Directory'.ljust(15),"".center(2),'Status Code'.ljust(12),'URI')
                for num,t in enumerate(responces):
                    if t.status == 200:                     
                        #result.append((directories[num],t))
                        print(str(directories[num]).ljust(15),"=>".center(2),str(t.status).ljust(12),str(t.url))
                        
                     
        except KeyboardInterrupt:
            print("KeyboardInterrupt Closing...")     
        except Exception as E:
            print(f'{E}\n closing...')
            sys.exit()

    # Running Async event loop/run function
    asyncio.run(get_session())
    
    # Preety Output
    #print('\n')
    #print('[+] Getting Response From Reqquests')
    #print('[+] Listing Results Only For Status Code 200\n')
    #print('Directory'.ljust(15),"".center(2),'Status Code'.ljust(3))
    #for i in result:
     #   if i[1].status == 200:
      #      #r = i.text()
       #     print(str(i[0]).ljust(15),"=>".center(2),str(i[1].status).ljust(3))
            
start = time.time()   

try:
    main()
except KeyboardInterrupt:
    print("KeyboardInterrupt Closing...")
except:
    print("Something went wrong try again")
    sys.exit()

print('\ntook',time.time()-start)



               
#async def get_dir():
#    async with aiohttp.ClientSession() as session:
#        for directory in directories:
#            print(f"trying --> {directory}",end='\r',flush=True)
#            result = await session.get(url.format(directory),ssl=False)
#            if result.status == 200:
#                print(f"{directory} present")
        
# event loop
#loop = asyncio.get_event_loop()
#loop.run_until_complete(get_dir())
#loop.close()
# same as running asyncio.run()
