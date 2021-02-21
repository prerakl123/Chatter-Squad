from tkinter import *
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import emoji
import random
from customwidgets import PlaceHolderText


class CZClient(Tk):
    EMOJI_NAMES = list(emoji.EMOJI_ALIAS_UNICODE_ENGLISH.keys())
    EMOJI_FIGURES = list(emoji.EMOJI_ALIAS_UNICODE_ENGLISH.values())
    BUFSIZ = 1024

    def __init__(self, host='127.0.0.1', port=33000):
        Tk.__init__(self)
        self.messages_frame = Frame(self)
        self.scrollbar = Scrollbar(self.messages_frame)  # To navigate through past messages.

        # Following will contain the messages.
        self.msg_list = Text(self.messages_frame, yscrollcommand=self.scrollbar.set, insertbackground='white',
                             font=('Segoe UI Emoji', 12), insertofftime=0)
        self.alphabet_color = {}
        for i in range(26):
            color = '#%02x%02x%02x' % (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))
            if len(color) > 7:
                color = color[:7]
            self.alphabet_color[f"username-{chr(97+i)}"] = color
        self.alphabet_color['username-s_char'] = '#%02x%02x%02x' % (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))
        self.alphabet_color['username-s_char'] = self.alphabet_color['username-s_char'][:7]

        for i in self.alphabet_color.keys():
            self.msg_list.tag_config(i, foreground=self.alphabet_color[i], background='gray84')
        self.msg_list.tag_config('clicked_line', background='gray50')
        for i in ['<Any-Key>', '<Delete>', '<BackSpace>']:
            self.msg_list.bind(i, lambda _=None: 'break')
        self.msg_list.bind('<ButtonRelease-1>', self.on_click)
        self.msg_clicked = False
        self.msg_clicked_ind = None

        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.msg_list.pack(side=LEFT, fill=BOTH, expand=True)
        self.messages_frame.pack(side=TOP, fill=BOTH, expand=True)

        self.msg_entry_frame = Frame(self)
        self.button_frame = Frame(self)
        self.entry_field = PlaceHolderText(self.msg_entry_frame, bgtext='Send Message...', height=2,
                                           font=('Times New Roman', 12))
        self.entry_field.bind("<Return>", self.send_message)
        self.entry_field.bind('<Shift-Return>', self.on_shift_return)
        self.entry_field.pack(fill=BOTH, expand=True, side=LEFT)
        self.send_button = Button(self.button_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=TOP, fill=BOTH, expand=True)
        self.emoji_button = Button(self.button_frame, text=u"\U0001f642", font=('Segoe UI Symbol', 13),
                                   command= lambda _=None: self.show_emoji_win(field=self.entry_field))
        self.emoji_button.pack(side=BOTTOM, fill=BOTH, expand=True)
        self.button_frame.pack(side=RIGHT, fill=BOTH)
        self.msg_entry_frame.pack(side=BOTTOM, fill=BOTH, expand=True)

        self.bind('<Control-Shift-E>', lambda _=None: self.show_emoji_win(field=self.entry_field))
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect((host, port))

    def colorize(self, msg='', ind=END):
        rows = msg.count('\n') + 1
        uname_ind = msg.find(':\n')
        if uname_ind < 0:
            return
        uname = msg[:uname_ind]
        if uname[1].lower() in [chr(i) for i in range(97, 123)]:
            self.msg_list.tag_add(f'username-{uname[1].lower()}', ind, f"{ind} lineend")
        else:
            self.msg_list.tag_add(f'username-s_char', ind, f"{ind} lineend")

    def on_click(self, event=None):
        cur_line_ind = f"{self.msg_list.index(INSERT).split('.')[0]}.0"
        if int(cur_line_ind.split('.')[0]) < 4:
            return 'break'
        if self.msg_clicked is True:
            if cur_line_ind == self.msg_clicked_ind:
                self.msg_list.tag_remove('clicked_line', 1.0, END)
                self.msg_clicked = False
                self.msg_clicked_ind = None
                return
            self.msg_list.tag_remove('clicked_line', 1.0, END)
            self.msg_list.tag_add('clicked_line', f"{cur_line_ind.split('.')[0]}.0", f"{cur_line_ind} lineend+1c")
            self.msg_clicked_ind = cur_line_ind
        elif self.msg_clicked is False:
            self.msg_list.tag_add('clicked_line', f"{cur_line_ind.split('.')[0]}.0", f"{cur_line_ind} lineend+1c")
            self.msg_clicked_ind = cur_line_ind
            self.msg_clicked = True
        

    def on_closing(self, event=None):
        """This function is to be called when the window is closed."""
        self.entry_field.delete(1.0, END)
        self.entry_field.insert(1.0, "{quit}")
        self.send_message()
        self.destroy()

    def on_shift_return(self, event=None):
        self.entry_field.insert(INSERT, '\n')
        self.entry_field.see(INSERT)
        return 'break'

    def receive(self):
        """Handles receiving of messages."""
        while True:
            try:
                msg = self.client_socket.recv(self.BUFSIZ).decode("utf8")
                self.msg_list.mark_set(INSERT, END)
                ind = self.msg_list.index(INSERT+' +1c')
                self.msg_list.insert(END, msg)
                self.msg_list.see(END)
                self.colorize(msg, ind)
            except OSError:  # Possibly client has left the chat.
                break

    def send_message(self, event=None):  # event is passed by binders.
        """Handles sending of messages."""
        msg = self.entry_field.get(1.0, END).lstrip().rstrip()
        self.entry_field.delete(1.0, END)  # Clears input field.
        if msg in ['{emoji}', '\\em', '\\emoji']:
            self.show_emoji_win(self.entry_field)
            return 'break'
        self.client_socket.send(bytes(emoji.emojize(msg), "utf8"))
        if msg == ["{quit}", '\\q', '\\quit', '{exit}', '\\exit', '\\e']:
            self.client_socket.close()
            self.quit()
            return 'break'
        return 'break'

    def show_emoji_win(self, field):
        def insert_into_field(event=None):
            n = emoji_listbox.get(emoji_listbox.curselection()[0])
            field.insert('insert', self.EMOJI_NAMES[self.EMOJI_FIGURES.index(n)])
            
        root_top = Toplevel(self)
        root_top.geometry('400x500+1+1')
        root_top.title('Select Emoji')
        emoji_listbox = Listbox(root_top, font=('Segoe UI Emoji', 14))
        emoji_listbox.pack(fill=BOTH, expand=True)
        for i in range(len(self.EMOJI_FIGURES)):
            emoji_listbox.insert(END, f"{self.EMOJI_FIGURES[i]}")
        emoji_listbox.bind('<Double-1>', insert_into_field)


if __name__ == '__main__':
    root = CZClient()
    receive_thread = Thread(target=root.receive)
    receive_thread.start()
    root.mainloop()






# """Script for Tkinter GUI chat client."""
# from socket import AF_INET, socket, SOCK_STREAM
# from threading import Thread
# from tkinter import *
# import emoji
#
# EMOJI_NAMES = list(emoji.EMOJI_ALIAS_UNICODE_ENGLISH.keys())
# EMOJI_FIGURES = list(emoji.EMOJI_ALIAS_UNICODE_ENGLISH.values())
#
#
# def receive():
#     """Handles receiving of messages."""
#     while True:
#         try:
#             msg = client_socket.recv(BUFSIZ).decode("utf8")
#             msg_list.insert(END, msg)
#         except OSError:  # Possibly client has left the chat.
#             break
#
#
# def send(event=None):  # event is passed by binders.
#     """Handles sending of messages."""
#     msg = my_msg.get()
#     my_msg.set("")  # Clears input field.
#     if msg in ['{emoji}', '\\e', '\\emoji']:
#         show_emoji_win(entry_field)
#         return
#     client_socket.send(bytes(emoji.emojize(msg), "utf8"))
#     if msg == ["{quit}", '\\q', '\\quit', '{exit}', '\\exit']:
#         client_socket.close()
#         top.quit()
#
#
# def on_closing(event=None):
#     """This function is to be called when the window is closed."""
#     my_msg.set("{quit}")
#     send()
#     top.destroy()
#     exit()
#
#
# def show_emoji_win(field):
#     def insert_into_field(event=None):
#         n = emoji_listbox.get(emoji_listbox.curselection()[0])
#         field.insert('insert', n.split()[0])
#
#     root_top = Toplevel(top)
#     root_top.geometry('300x500+1+1')
#     root_top.title('Select Emoji')
#     emoji_listbox = Listbox(root_top, font=('Segoe UI Emoji', 14))
#     emoji_listbox.pack(fill=BOTH, expand=True)
#     for i in range(len(EMOJI_FIGURES)):
#         emoji_listbox.insert(END, f"{EMOJI_NAMES[i]}\t{EMOJI_FIGURES[i]}")
#     emoji_listbox.bind('<Double-1>', insert_into_field)
#
#
# top = Tk()
# top.title("Chatter")
#
# messages_frame = Frame(top)
# my_msg = StringVar()  # For the messages to be sent.
# my_msg.set("Type your messages here.")
# scrollbar = Scrollbar(messages_frame)  # To navigate through past messages.
# # Following will contain the messages.
# msg_list = Listbox(messages_frame, height=20, width=140, yscrollcommand=scrollbar.set,
#                    font=('Segoe UI Emoji', 12))
# scrollbar.pack(side=RIGHT, fill=Y)
# msg_list.pack(side=LEFT, fill=BOTH, expand=True)
# messages_frame.pack(fill=BOTH, expand=True)
#
# entry_field = Entry(top, width=105, textvariable=my_msg, font=('Times New Roman', 12))
# entry_field.bind("<Return>", send)
# entry_field.pack()
# send_button = Button(top, text="Send", command=send)
# send_button.pack()
#
# top.protocol("WM_DELETE_WINDOW", on_closing)
#
# # ----Now comes the sockets part----
# HOST = input('Enter host: ')
# PORT = input('Enter port: ')
# if not PORT:
#     PORT = 33000
# else:
#     PORT = int(PORT)
# if not HOST:
#     HOST = '127.0.0.1'
# else:
#     HOST = HOST
#
# BUFSIZ = 1024
# ADDR = (HOST, PORT)
#
# client_socket = socket(AF_INET, SOCK_STREAM)
# client_socket.connect(ADDR)
#
# receive_thread = Thread(target=receive)
# receive_thread.start()
# mainloop()
