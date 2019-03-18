import socket, sys
import _thread



def log_info(message):
    logger_file = open("logs.txt", "a")
    logger_file.write(message)
    logger_file.close()

try:
    listening_port = 8002
    print("haha started :)))")
except KeyboardInterrupt:
    # print("\n[*] user requested an interrupt")
    # print("[*] application exiting ... ")

    message = "[*] user requested an interrupt" + " \n"
    log_info(message)
    message = "[*] application exiting ... " + " \n"
    log_info(message)

    sys.exit()

max_conn = 5 #max connection queus to hold
buffer_size = 4096 #max socket buffer size

def start(user_filter_list):
    # try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #initiate socket
    s.bind(('',listening_port)) #bind socket to listen
    s.listen(max_conn) #start listening for incoming connections
    # print("[*] initializing sockets ... done")
    # print("[*] sockets binded successfully")
    # print("[*] proxyserver started successfully [%d] \n" %listening_port)

    message = "[*] initializing sockets ... done" + " \n" + "[*] sockets binded successfully" + "\n" + "[*] proxyserver started successfully [%d] \n" %listening_port
    log_info(message)

    # except Exception as e:
    #     print("[*] unable to initialize socket ")
    #     sys.exit(1)

    while 1 :
        try:
            conn, addr = s.accept() # accept connection from client browser
            data = conn.recv(buffer_size) #recieve client data
            # print("[*] client browser request came to proxy")
            message = "[*] client browser request came to proxy" + " \n"
            log_info(message)
            _thread.start_new_thread(conn_string, (conn, data, addr, user_filter_list))

        except KeyboardInterrupt:
            s.close()
            message = "[*]proxy server shutting down..." + " \n"
            log_info(message)
            # print("\n[*]proxy server shutting down...")
            sys.exit(1)
    s.close()

def conn_string(conn, data, addr, user_filter_list):
    #client browser request appears here
    try:
        print("data is " + "\n")
        print(data)
        print("\n")
        # data = data.decode()
        first_line = data.split('\n'.encode())[0]
        url = first_line.split(' '.encode())[1]

        http_pos = url.find("://".encode())
        if http_pos == -1:
            temp = url
        else:
            temp = url[(http_pos + 3):]
        port_pos = temp.find(":".encode())
        webserver_pos = temp.find("/".encode())
        if webserver_pos == -1:
            webserver_pos = len(temp)
        webserver = ""
        port = -1
        if port_pos == -1 or webserver_pos < port_pos:
            # default port
            port = 80
            webserver = (temp[:webserver_pos]).decode()
        else:
            # specifiec port
            port = int((temp[(port_pos + 1):])[:webserver_pos - port_pos - 1])
            webserver = (temp[:port_pos]).decode()

        proxy_server(webserver, port, conn, addr, data, user_filter_list)
    except Exception:
        pass


def proxy_server(webserver, port, conn, addr, data, user_filter_list):
    try:
        flag = True
        for category in user_filter_list :
            for address in category:
                # print("[****************************]web server : {}".format(webserver))
                # print("[****************************]address : {}".format(address))
                if address.__contains__(webserver):
                    file = open("filter.html", "r")
                    lines = file.readlines()
                    txt = ''.join(lines)
                    txt = txt.encode()
                    conn.send(txt)
                    conn.close()
                    flag = False
                    break
        if flag:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((webserver, port))
            # data = data.encode()
            s.send(data)

            while 1:
                # read response from server
                response = s.recv(buffer_size)

                if len(response) > 0:
                    conn.send(response)
                    print("[*] hale cheshmat :*** ")

                else:
                    break

            s.close()
            conn.close()

    except socket.error:
        s.close()
        conn.close()
        sys.exit(1)


# start(user_filter_list=[])
from tkinter import *

class MyFirstGUI:
    def __init__(self, master):
        self.num_cat = 0
        self.i = 0
        self.cat_list = []
        self.adds_list = []

        self.entered_list = []
        self.final_list = []

        self.master = master
        master.title("Filtering Proxy GUI")

        T = Text(root, height=1)
        T.grid(row=self.i, columnspan=3)
        T.insert(END, "Do the following and at the end press start")
        # self.label = Label(master, text="do the following and at the end press start").grid(row=self.i)

        self.start_button = Button(master, text="start", command=self.start_proxy)
        # self.greet_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        # self.close_button.pack()

        # self.label_num = Label(master, text=" enter num of gategories and press submit").grid(row=self.i)
        # self.e1 = Entry(master)
        # self.e1.grid(row=self.i, column=1)
        # self.submit_button = Button(master, text="submit", command=self.submit).grid(row=self.i, column=2)

        self.i = self.i + 1
        self.label_num = Label(master, text="enter a gategory name and press create").grid(row=self.i)
        self.e2 = Entry(master)
        self.e2.grid(row=self.i, column=1)
        self.create_button = Button(master, text="create", command=self.create).grid(row=self.i, column=2)




        self.start_button.grid(row=20)
        self.close_button.grid(row=21)

    # def submit(self):
    #     if self.num_cat == 0:
    #         self.i = self.i + 1
    #         self.choose_cat_button = Button(self.master, text="choose a category", command=self.choose).grid(row=self.i)
    #     self.num_cat = self.e1.get()
    #     print("num of categories is : {}".format(self.num_cat))


    def choose(self):
        self.vars = []
        self.i = self.i + 1
        T = Text(root, height=1)
        T.grid(row=self.i)
        T.insert(END, "after selecting please press Done button and then press start to run the proxy")
        # Label(self.master, text="after selecting please press Done button").grid(row=self.i)
        for j in range(0, len(self.cat_list)):
            self.i = self.i + 1
            self.vars.append(IntVar())
            Checkbutton(self.master, text=self.cat_list[j] , variable=self.vars[j]).grid(row=self.i, sticky=W)

        # self.i = self.i + 1
        self.choose_cat_button = Button(self.master, text="Done", command=self.make_final_list).grid(row=self.i)

    def make_final_list(self):

        for k in range(0, len(self.vars)):
            if self.vars[k].get() == 1 :
                self.final_list.append(self.entered_list[k])

    def create(self):
        if self.e2.get() not in self.cat_list:
            self.cat_list.append(self.e2.get())
            self.entered_list.append([])
            print("category *** {} *** created ".format(self.e2.get()))
        else:
            print("address is duplicate so please add address:|")
        if len(self.cat_list) > 1:
            pass
        else:
            self.i = self.i + 1
            self.insertadd_button = Button(self.master, text="insert address for your category",
                                           command=self.insert).grid(row=self.i)

    def insert(self):

        if len(self.adds_list) > 0 :
            pass
        else:
            self.i = self.i + 1
            self.label_add = Label(self.master, text="add an address and press add").grid(row=self.i)
            self.e3 = Entry(self.master)
            self.e3.grid(row=self.i, column=1)
            self.add_button = Button(self.master, text="add", command=self.add).grid(row=self.i, column=2)

        self.i = self.i + 1
        self.label = Label(self.master,
                           text="choose the categories you want to filter :D and then press Done")
        self.label.grid(row=self.i, columnspan=2, sticky=W)
        self.i = self.i + 1
        self.choose_cat_button = Button(self.master, text="choose a category", command=self.choose).grid(row=self.i)


    def add(self):
        if self.e3.get() not in self.adds_list:
            self.adds_list.append(self.e3.get())
            print(" address {1} added to category {0}".format(self.e2.get(), self.e3.get()))
            cat = self.cat_list.index(self.e2.get())
            # print("cat is {}".format(cat))
            # print("catlist is {}".format(self.cat_list))
            self.entered_list[cat].append(self.e3.get())
        else:
            print("address is duplicate :|")

    def start_proxy(self):
        self.start_button["text"]="connected"
        print("\nkhoooooob entered list ine {} \n".format(self.entered_list))
        print("\nkhoooooob final list ine {} \n".format(self.final_list))
        start(self.final_list)



root = Tk()
my_gui = MyFirstGUI(root)
root.mainloop()