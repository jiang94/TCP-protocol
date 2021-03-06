from tkinter import *

TITLE_FONT = ("Helvetica", 18, "bold")


class App(Tk):

    tcp = None

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        label = Label(self, text="TCP OP")
        label.pack()

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (ClosedFrame, ListenFrame, SYNReceivedFrame, SYNSentFrame, EstablishedFrame):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("ClosedFrame")

    def set_tcp(self, tcp):
        self.tcp = tcp

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def change_state_closed(self, *args):  # on a besoin du *args pour le call via event
        self.show_frame("ClosedFrame")

    def change_state_listen(self, *args):
        self.show_frame("ListenFrame")

    def change_state_syn_received(self, *args):
        self.show_frame("SYNReceivedFrame")

    def change_state_syn_sent(self, *args):
        self.show_frame("SYNSentFrame")

    def change_state_established(self, *args):
        self.show_frame("EstablishedFrame")


class ClosedFrame(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="State : Closed", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)

        labelframe = LabelFrame(self, text="Passive OPEN")
        labelframe.pack()
        labal2 = Label(labelframe, text="source port : ")
        labal2.pack()
        spinbox = Spinbox(labelframe, from_=0, to_=9999)
        spinbox.pack()
        button = Button(labelframe, text="Open",
                           command=lambda: controller.tcp.closed_open(int(spinbox.get())))
        button.pack()

        labelframe2 = LabelFrame(self, text="Active OPEN")
        labelframe2.pack()
        labal4 = Label(labelframe2, text="source port : ")
        labal4.pack()
        spinbox3 = Spinbox(labelframe2, from_=0, to_=9999)
        spinbox3.pack()
        labal3 = Label(labelframe2, text="destination port : ")
        labal3.pack()
        spinbox2 = Spinbox(labelframe2, from_=0, to_=9999)
        spinbox2.pack()

        button2 = Button(labelframe2, text="Send",
                           command=lambda: controller.tcp.closed_send(int(spinbox2.get()), int(spinbox3.get())))
        button2.pack()


class ListenFrame(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="State : Listen", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)

        labelframe = LabelFrame(self, text="SEND")
        labelframe.pack()
        label2 = Label(labelframe, text="destination port : ")
        label2.pack()
        spinbox = Spinbox(labelframe, from_=0, to_=9999)
        spinbox.pack()
        button = Button(labelframe, text="Send SYN",
                           command=lambda: controller.tcp.listen_send_syn(int(spinbox.get())))
        button.pack()

        button2 = Button(self, text="Receive SYN",
                           command=lambda: controller.show_frame("SYNReceivedFrame"))
        button2.pack()


class SYNSentFrame(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="State : SYN-Sent", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)
        '''button = Button(self, text="Receive SYN+ACK, Send ACK",
                           command=lambda: controller.show_frame("EstablishedFrame"))
        button.pack()
        labelframe = LabelFrame(self, text="Simultaneous Open")
        labelframe.pack()
        button2 = Button(labelframe, text="Receive SYN, Send ACK",
                           command=lambda: controller.show_frame("SYNReceivedFrame"))
        button2.pack()'''


class SYNReceivedFrame(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="State : SYN-Received", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)
        button = Button(self, text="Send SYN + ACK",
                           command=lambda: controller.tcp.syn_received_send_syn_ack())
        button.pack()


class EstablishedFrame(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="State : Established", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)

        labelframe = LabelFrame(self, text="Send data")
        labelframe.pack()
        entry = Entry(labelframe)
        entry.pack()

        def send_button_clicked():
            controller.tcp.send_data(entry.get())
            entry.delete(0,END)
        button = Button(labelframe, text="Send", command=send_button_clicked)
        button.pack()

        button = Button(self, text="Close, Send FIN",
                           command=lambda: controller.show_frame("ListenFrame"))
        button.pack()


def startapp():
    app = App()
    app.mainloop()