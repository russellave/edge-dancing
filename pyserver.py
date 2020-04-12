'''
Bluetooth socket support

Copyright 2018  Gunnar Bowman, Emily Boyes, Trip Calihan, Simon D. Levy, Shepherd Sims

MIT License
'''

import os

import bluetooth as bt

from playsound import playsound
import pygame
import time
from csv_manager import getLightsAndTimes, getLightsAndTimesFeroze, getColorInfo



class BluetoothServer(object):
    '''
    Provides an abstract class for serving sockets over Bluetooth.  You call the constructor and the start()
    method.  You must implement the method handleMessage(self, message) to handle messages from the client.
    '''

    def __init__(self):
        '''
        Constructor
        '''

        # Arbitrary service UUID to advertise
        self.uuid = "7be1fcb3-5776-42fb-91fd-2ee7b5bbb86d"
        self.play_music = False
        self.client_sock = None

    def start(self, audio_file_input, csv_file_input):
        '''
        Serves a socket on the default port, listening for clients.  Upon client connection, runs a loop to 
        that receives period-delimited messages from the client and calls the sub-class's 
        handleMessage(self, message) method.   Sub-class can call send(self, message) to send a 
        message back to the client.   Begins listening again after client disconnects.
        '''

        # Make device visible
        os.system("hciconfig hci0 piscan")

        # Create a new server socket using RFCOMM protocol
        server_sock = bt.BluetoothSocket(bt.RFCOMM)

        # Bind to any port
        server_sock.bind(("", bt.PORT_ANY))

        # Start listening
        server_sock.listen(1)

        # Get the port the server socket is listening
        port = server_sock.getsockname()[1]

        # Start advertising the service
        bt.advertise_service(server_sock, "RaspiBtSrv",
                           service_id=self.uuid,
                           service_classes=[self.uuid, bt.SERIAL_PORT_CLASS],
                           profiles=[bt.SERIAL_PORT_PROFILE])

        # Outer loop: listen for connections from client

        while True:

            print("Waiting for connection on RFCOMM channel %d" % port)

            try:

                # This will block until we get a new connection
                self.client_sock, client_info = server_sock.accept()
                print("Accepted connection from " +  str(client_info))
                
                s = ''
                index = 0
                curr_state = "aaaaaaaaaaaaaaa" #all black output (assuming a is black)

                input_times = [0] * 15 # Instantiates button input list

                # messages,times = getLightsAndTimes(file=csv_file_input, initial_state=curr_state)
                # messages,times = getLightsAndTimes()
                color2char, char2rgb = getColorInfo()
                messages, times = getLightsAndTimesFeroze(file=csv_file_input, initial_state=curr_state, color2char=color2char)
                is_started = False
                start_time = time.time()
                while True:                    
                    if is_started: 
                        current_time = time.time()
                        time_diff = current_time - start_time
                        time_stamp = times[index]  
                        
                        if time_diff > time_stamp:

                            curr_state = set_current_state(curr_state, input_times, current_time, messages[index])
                            self.send(curr_state)

                            # self.send(messages[index])      
                            # curr_state = messages[index]

                            index  = (index+1)%len(messages)	
#                    start_read = time.time()
                    c = self.client_sock.recv(1).decode('utf-8')

                    #Full string read->do soemthing
                    if c == '.' and len(s) > 0:
                        if s == "color" and not is_started: 
                            self.send(char2rgb)
                        elif s == "start" and not is_started: 
                            start_time = time.time()
                            is_started = True
                            pygame.mixer.init()
                            pygame.mixer.music.load(audio_file_input)
                            # pygame.mixer.music.load("renegade.mp3")
                            pygame.mixer.music.play()
                        elif not s== ".": 
                            curr_state, input_times = self.handleTouch(s, curr_state, current_time, input_times)
                        s = ''                    
                    else:
                        s += c
                    end_read = time.time()
#                    print("READING DELAY IS: "+str(start_read-end_read))
            except IOError:
                pass

            except KeyboardInterrupt:

                if self.client_sock is not None:
                    self.client_sock.close()

                server_sock.close()

                print("Server going down")
                break

    def send(self, message):
        '''
        Appends a period to your message and sends the message back to the client.
        '''
        
        self.client_sock.send((message+'.').encode('utf-8'))

    def set_current_state(curr_state, input_times, current_time, message_string):
        message_char_list = list(message_string)

        i = 0

        while i < len(message_char_list):
            if input_times[i] > current_time:
                message_char_list[i] = curr_state[i]

            i += 1

        return ''.join(message_char_list)





