from tkinter import *
import tkinter.messagebox as tk_mb
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
import json


class CZServer(Tk):
    def __init__(self, host='127.0.0.1', port=33000):
        Tk.__init__(self)
        self.connections = 0
        self.clients = {}
        self.addresses = {}

        self.title('Server Log')
        self.log_text = Text(self, bd=0, bg='black', fg='white', font=('Consolas', 8))
        self.log_text.pack(expand=True, fill=BOTH)
        self.log_text.after(200, self.check_log)
        for i in ['<BackSpace>', '<Delete>', '<Return>', '<Any-Key>']:
            self.log_text.bind(f"{i}", lambda _=None: 'break')

        with open('server_logs.json', 'r') as file:
            self.log_dict = json.load(file)
        date = f"{time.ctime(time.time()).split()[1]},{time.ctime(time.time()).split()[2]}," \
               f"{time.ctime(time.time()).split()[4]}"
        if date in list(self.log_dict.keys()):
            pass
        else:
            self.log_dict[f"{time.ctime(time.time()).split()[1]},{time.ctime(time.time()).split()[2]},"
                          f"{time.ctime(time.time()).split()[4]}"] = {'joined': {}, 'left': {}}
        self.write_logs()

        self.SERVER = socket(AF_INET, SOCK_STREAM)
        self.SERVER.bind((host, port))
        self.BUFSIZ = 1024
        # print(self.SERVER.getsockname(), self.SERVER.get_inheritable())

    def accept_incoming_connections(self):
        """Sets up handling for incoming clients."""
        while True:
            client, client_address = self.SERVER.accept()
            # self.log_text.insert(END, "%s:%s has connected.\n" % (client_address[0], client_address[1]))
            self.connections += 1
            client.send(bytes("Greetings Human! Type your name and press enter to start chatting!\n", "utf8"))
            self.addresses[client] = client_address
            Thread(target=self.handle_client, args=(client,)).start()

    def broadcast(self, msg, prefix=""):  # prefix is for name identification.
        """Broadcasts a message to all the clients."""
        for sock in self.clients:
            sock.send(bytes(prefix, "utf8") + msg)

    def check_log(self, event=None):
        """Checks and applies tags to log text"""
        if self.connections > 0:
            if self.log_text.get(1.0, '1.0 lineend') == 'Waiting for connection...':
                self.log_text.delete(1.0, '1.0 lineend+1c')

            row = 1
            while row != int(self.log_text.index(END).split('.')[0]):
                linetext = list(self.log_text.get(f"{row}.0", f"{row}.0 lineend").split(' '))
                ip_ind = self.log_text.search(linetext[0], f"{row}.0", f"{row}.0 lineend")

                if 'disconnected.' in linetext:
                    self.log_text.tag_add('disconnected', f"{row}.0", f"{row}.0 lineend")
                elif 'connected.' in linetext:
                    self.log_text.tag_add('connected', f"{row}.0", f"{row}.0 lineend")

                row += 1

            self.log_text.tag_config('connected', foreground='green')
            self.log_text.tag_config('disconnected', foreground='red')

        elif 'Waiting for connection...' in self.log_text.get(1.0, '1.0 lineend'):
            self.log_text.tag_add('wait_connection', '1.0', '1.0 lineend')
            self.log_text.tag_config('wait_connection', foreground='gray18', font='Consolas 8 italic')

        self.after(2000, self.check_log)

    def handle_client(self, client):  # Takes client socket as argument.
        """Handles a single client connection."""
        while True:
            try:
                name = client.recv(self.BUFSIZ).decode("utf8")
                if name == '{quit}' or name.find('\n') > 0 or name.find('\t') > 0:
                    raise ValueError
                else:
                    break
            except ValueError:
                tk_mb.showerror('NameError!', 'Invalid Name:\nName cannot contain newline or tab character.\nTry again')

        welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.\n' % name
        client.send(bytes(welcome, "utf8"))
        msg = "%s has joined the chat!\n" % name
        self.broadcast(bytes(msg, "utf8"))
        client_ip = client.getpeername()
        self.log_text.insert(END, f"{time.ctime(time.time()).split()[3]}: " + "{%s} " % name +
                             f"{client_ip} has connected.\n")
        # print(client.getsockname(), client.get_inheritable(), client.__str__())
        cur_time = time.ctime(time.time()).split()
        self.log_dict[f"{cur_time[1]},{cur_time[2]},{cur_time[4]}"]['joined'][f"{cur_time[3]}"] = name
        self.clients[client] = name

        while True:
            msg = client.recv(self.BUFSIZ)
            if msg != bytes("{quit}", "utf8"):
                self.broadcast(msg, '\n' + name + ":\n")
            else:
                client.send(bytes("{quit}", "utf8"))
                client.close()
                self.log_text.insert(END, f"{time.ctime(time.time()).split()[3]}: " + "{%s} " % self.clients[client] +
                                     f"{client_ip} has disconnected.\n")
                del self.clients[client]
                cur_time = time.ctime(time.time()).split()
                self.log_dict[f"{cur_time[1]},{cur_time[2]},{cur_time[4]}"]['left'][f"{cur_time[3]}"] = name
                self.broadcast(bytes("%s has left the chat.\n" % name, "utf8"))
                break

    def write_logs(self, event=None):
        with open('server_logs.json', 'w') as file:
            json_object = json.dumps(self.log_dict, indent=2)
            file.write(json_object)
        self.after(5000, self.write_logs)


def main():
    root = CZServer()
    root.geometry('500x500')
    root.SERVER.listen(5)
    accept_thread = Thread(target=root.accept_incoming_connections)
    accept_thread.start()
    root.log_text.insert('1.0', 'Waiting for connection...\n')
    # root.after(6000, lambda _=None: accept_thread.join())
    root.mainloop()
    accept_thread.join()
    root.SERVER.close()


if __name__ == '__main__':
    main()









# """Server for multithreaded (asynchronous) chat application."""
# from socket import AF_INET, socket, SOCK_STREAM
# from threading import Thread
#
#
# def accept_incoming_connections():
#     """Sets up handling for incoming clients."""
#     while True:
#         client, client_address = SERVER.accept()
#         print("%s:%s has connected." % (client, client_address))
#         client.send(bytes("Greetings from the cave! Now type your name and press enter!", "utf8"))
#         addresses[client] = client_address
#         Thread(target=handle_client, args=(client,)).start()
#
#
# def handle_client(client):  # Takes client socket as argument.
#     """Handles a single client connection."""
#
#     name = client.recv(BUFSIZ).decode("utf8")
#     welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
#     client.send(bytes(welcome, "utf8"))
#     msg = "%s has joined the chat!" % name
#     broadcast(bytes(msg, "utf8"))
#     clients[client] = name
#
#     while True:
#         msg = client.recv(BUFSIZ)
#         if msg != bytes("{quit}", "utf8"):
#             broadcast(msg, name + ": ")
#         else:
#             client.send(bytes("{quit}", "utf8"))
#             client.close()
#             del clients[client]
#             broadcast(bytes("%s has left the chat." % name, "utf8"))
#             break
#
#
# def broadcast(msg, prefix=""):  # prefix is for name identification.
#     """Broadcasts a message to all the clients."""
#
#     for sock in clients:
#         sock.send(bytes(prefix, "utf8") + msg)
#
#
# clients = {}
# addresses = {}
#
# HOST = '127.0.0.1'
# PORT = 33000
# BUFSIZ = 1024
# ADDR = (HOST, PORT)
#
# SERVER = socket(AF_INET, SOCK_STREAM)
# SERVER.bind(ADDR)
#
# if __name__ == "__main__":
#     SERVER.listen(5)
#     print("Waiting for connection...")
#     ACCEPT_THREAD = Thread(target=accept_incoming_connections)
#     ACCEPT_THREAD.start()
#     ACCEPT_THREAD.join()
#     SERVER.close()
