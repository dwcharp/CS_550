from Peer import Client
from MetaData import *
import random
import string
import socket
import time
import Pyro4
import os

#### This the driver class that helps run a client.


num_clients = 10
clients = []
max_file_size = 3000 #  max_file_size * file_name to keep things i.e "a" * 2 = "aa"
max_num_files = 10
file_names = []

def main():
    create_random_file_names()
    create_many_clients()
    user_input()

####command prompt to allow a user to run a client
def user_input():
    while True:
        print "1) List Files in Index\n2) List Files on this Server\n3) Get a File From Index\n4) Delete File\n5) Shutdown Client"
        selection = raw_input("Enter your input: ")

        if selection == "1":
            print "Files in Index"
            list_in_index()

        elif selection == "2" :
            print "Your Files:"
            list_files_on_client()

        elif selection == "3" :
            print "Which File: "
            fn = raw_input("Enter your input:\n")
            test_get_file(fn)

        elif selection == "4" :
            print "Which File: "
            f= raw_input("Enter your input:\n")
            delete_file(f)

        elif selection == "5" :
            stop_clients()
            print "GoodBye\n"
            break


#### Ask the client to contact the Index Server for a list of files
def list_in_index():
    for klient in clients:
        klient.list_files_on_index()

#### have the client download the file
def test_get_file(file_name):
    c1 = clients[1]
    print "Testing with file " + file_name
    c1.obtain(file_name)


def list_files_on_client():
    clients[0].list_files_on_index()

def delete_file(file_name):
    client = clients[0]
    client.delete_file(file_name)



def createSingleClient(id_num):
    client = Client(id_num)
    client.set_meta_data(create_files(id_num))
    #client.start_client()
    clients.append(client)
    return client

def create_many_clients():
    file  = open("star_topolgy.txt")
    clients_dict = dict()
    while 1 :
        info = file.readline()
        if not info:
            break
        else:
            info = info.strip("\n")
            info = info.split(",")
            #print info
            c = info[0]
            del info[0]
            clients_dict[c] = info

    file.close()
    client_refs = dict()
    for k,v in clients_dict.items():
        #print k
        client = createSingleClient(k)
        client_refs[k] = client

    for klient in clients :
        for neigbhor in clients_dict[klient.id_num]:
            n_client = client_refs[neigbhor]
            klient.add_peer(n_client.ip_address,n_client)




#create random files for each client


def get_client(id):
    ns  = Pyro4.locateNS()
    uri = ns.lookup(id)
    print uri
    return Pyro4.Proxy(uri)

def stop_clients():
    for client in clients:
        client.stop_client()

def create_random_file_names():
    names = []
    for i in range(num_clients * 4):
        file_name = "file" + str(random.randint(0,50))
        while file_name in names:
            file_name =  "file" + str(random.randint(0,50))
        random_size = random.randint(1,max_file_size)
        names.append(file_name)
        file_names.append((file_name,random_size))

def create_file_contents(file_name,size):
    return file_name * size

def create_files(client_id):
    client_files = []
    files_picked = []
    directory = "test_files/"
    num_files_names = len(file_names) -1
    for i in range(1, max_num_files +1):
        file_name,size = file_names[random.randint(0,num_files_names)]
        while file_name in files_picked:
            file_name,size = file_names[random.randint(0,num_files_names)]
        files_picked.append(file_name)
        client_files.append(FileInfo(file_name,size))
        '''file  = open(directory + file_name + ".txt","wb+")
        file.write(create_file_contents(file_name,size) + "\n")
        file.close()'''
    return MetaData(directory,client_files)
if __name__=="__main__":
    main()

