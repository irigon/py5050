from libs import sdnv
import socket

class TCPCL_CL:

    def __init__(self, tcpcl_id):
        self.id = tcpcl_id
        self.header = self.create_header()
        self.connections=dict()
        self.next_hop = None

    def create_header(self):
        enc_id  = self.id.encode("ascii")
        enc_len = sdnv.encode(len(enc_id))
        return  b'dtn!\x03\x00\x00\x00\x05' + enc_len + enc_id

    def set_next_hop(self, selftcpcl_id):
        self.next_hop = selftcpcl_id

    # connect as client to a server. E.g: upcn
    # ignore if connection is already stablished
    def connect (self, sock, data):
        peer_id = data['peer_id']

    def reconnect(self, tcpcl_id):
        pass

    # for simplicity we just assume that socket will be able to send.
    def send(self, dst_id, msg):
        if type(msg) != bytes:
            print('Message should contain bytes')
            return
        print('Sending to {}: {}'.format(dst_id, msg))

    # receive data from network
    # on \0 shutdown, close socket and remove from connections
    def receive(self, sock, data):
        txt = sock.recv(1024)

        if not txt:
            print('Got disconnected. Cleaning up...')
            data['selector'].unregister(sock)
            sock.shutdown(socket.SHUT_RDWR)
            sock.close()

        print('Received {} on "receive"'.format(txt))




if __name__ == '__main__':
    cl = TCPCL_CL('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    print("{}".format(cl.header))
    pass
