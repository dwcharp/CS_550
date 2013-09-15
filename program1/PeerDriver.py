from Peer import Client
from MetaData import *
import random
import string
import socket
import time
import Pyro4

num_clients = 10
clients = []
max_file_size = 3000 #in chars
max_num_files = 5
file_names = []

def main():
    create_random_file_names()
    createClients(2)
    time.sleep(2)
    test_get_file()
    time.sleep(2)
    stop_clients()

def createClients(num_of_clients):

    num_clients = num_of_clients
    for i in range(num_of_clients):
        client = Client()
        client.set_meta_data(create_files(client.id_num))
        client.start_client()
        clients.append(client)

#create random files for each client

def test_get_file():
    c1 = get_client("1")
    c2 = get_client("2")
    print str(c1.get_id()) + "!!!!!!"
    name = c2.get_file_name()
    print "Testing with file " + name
    time.sleep(2)
    c1._pyroOneway.add("obtain")
    c1.obtain(name)

def get_client(id):
    ns  = Pyro4.locateNS()
    uri = ns.lookup(id)
    print uri
    return Pyro4.Proxy(uri)

def stop_clients():
    for client in clients:
        client.stop_client()

def create_random_file_names():
    for i in range(num_clients * 4):
        file_name = "file" + str(random.randint(0,100))
        file_names.append(file_name)

def create_file_contents(size):
    return ''.join(random.choice(string.ascii_letters) for x in range(size))

def create_files(client_id):
    client_files = []
    directory = "test_files/"
    num_files_names = len(file_names) -1
    for i in range(1, max_num_files +1):
        random_size = random.randint(1,max_file_size)
        file_name = file_names[random.randint(0,num_files_names)]
        client_files.append(FileInfo(file_name,random_size))
        file  = open(directory + file_name + ".txt","wb+")
        file.write(create_file_contents(random_size))
        file.close()
    return MetaData(directory,client_files)
if __name__=="__main__":
    main()

