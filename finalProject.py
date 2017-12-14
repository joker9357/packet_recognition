import copy

import pyshark

from packet_recognition.Packet import Packet


def main():
    cap = pyshark.FileCapture('./packet_recognition/1.cap')
    sum=0
    time = 0
    list_packet = []
    list_burst = []
    idx = 0
    for _ in cap:
        # print(_.ip.len)
        sum= sum + int(_.ip.len)
        length = float(_.captured_length)
        dst = str(_.layers[1].dst)
        src = str(_.layers[1].src)
        if idx == 0:
            time = float(_.sniff_timestamp)
            Packet.source = src
            Packet.destination = dst
            packet = Packet(src, dst, length)
            list_packet.append(packet)
        else:
            packet = Packet(src, dst, length)
            tmp_time = float(_.sniff_timestamp)
            if  tmp_time - time > 1:
                li = copy.copy(list_packet)
                list_burst.append(li)
                list_packet = []
                list_packet.append(packet)
                print("time: " + str(time))
            else:
                list_packet.append(packet)
            time = tmp_time
        idx += 1

    list_burst.append(list_packet)

    print("Total length of ip is "+str(sum))



if __name__=='__main__': main()