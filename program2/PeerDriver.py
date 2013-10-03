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
max_file_size = 3000 #in chars
max_num_files = 5
file_names = []

def main():
    create_random_file_names()
    createClients(1)
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
    client = clients[0]
    client.list_files_on_index()
    print "\n"

#### have the client download the file
def test_get_file(file_name):
    c1 = clients[0]
    print "Testing with file " + file_name
    c1.obtain(file_name)

#### List the files owned by the Server
def list_files_on_client():
    client = clients[0]
    files = client.get_file_names()
    for file in files:
        print file.name
    print "\n"

def delete_file(file_name):
    client = clients[0]
    client.delete_file(file_name)


#### Create X amount of clients, default is 1
def createClients(num_of_clients):

    num_clients = num_of_clients
    for i in range(num_of_clients):
        client = Client()
        client.set_meta_data(create_files(client.id_num))
        client.start_client()
        clients.append(client)

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
        file.write(create_file_contents(random_size) + "\n")
        file.close()
    return MetaData(directory,client_files)
if __name__=="__main__":
    main()

