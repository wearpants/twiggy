import socket as _socket

#XXX these need robustification for non-TCP sockets, etc.

def socket(self, s):
    ip_addr, port = s.getpeername()
    host, service = _socket.getnameinfo((ip_addr, port), 0)
    return self.fields(ip_addr=ip_addr, port=port, host=host, service=service)

def socket_minimal(self, s):
    ip_addr, port = s.getpeername()
    return self.fields(ip_addr=ip_addr, port=port)
