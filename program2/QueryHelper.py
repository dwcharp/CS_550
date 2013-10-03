class QueryHelper():
    def __init__(self,client):
        self.client = client

    #### This is called from other peers, and calls this on neigbhors

    def query(self,messageId,TTL,file_name,sender_info):
        if self.client.messages_received.has_key(messageId) or self.client.messages_sent.has_key(messageId):
            print "Not sending query from " + str(self.client.ip_address)
            return
        else:
            if self.client.ip_address == sender_info:
                self.client.messages_sent[messageId] = True
            else:
                self.client.messages_received[messageId] = sender_info
        if TTL > 0:
            TTL = TTL -1
            for peer in self.client.peers.values():
                peer.query(messageId,TTL,file_name,self.client.ip_address)

        if self.client.meta_data.has_file(file_name):
            self.client.send_hit_query(messageId,TTL,file_name,self.client.ip_address)
##### If peer as the file, send a hit query

    def send_hit_query(self,messageId,TTL,file_name,sender_info):
        print "Sending a Hit for: " + file_name + " from client: " + str(self.client.ip_address) + " orgin: " + str(sender_info)
        peer_info = self.client.messages_received[messageId]
        peer = self.client.peers[peer_info]
        peer.hit_query(messageId,TTL,file_name,sender_info)

    #### called from peer that is relaying a query message back
    def hit_query(self,messageId,TTL,file_name,sender_info):
        if self.client.messages_sent.has_key(messageId):
            print str(sender_info) + " has the file from client" + str(self.client.ip_address)
            #### download file
        else:
            self.client.send_hit_query(messageId,TTL,file_name,sender_info)
            pass

