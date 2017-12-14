import copy

import pyshark

from Packet import Packet


def main():
    cap = pyshark.FileCapture('1.cap')

    listburst = get_burst(cap)

    print("Total length of ip is "+str(sum))

def get_burst(cap):
    sum = 0
    time = 0
    list_up_packet = []
    list_down_packet = []
    list_bi_packet = []
    list_up_burst = []
    list_down_burst = []
    list_bi_burst = []
    idx = 0
    for _ in cap:
        # print(_.ip.len)
        sum += int(_.ip.len)
        length = float(_.captured_length)
        dst = str(_.layers[1].dst)
        src = str(_.layers[1].src)
        if idx == 0:
            time = float(_.sniff_timestamp)
            Packet.source = src
            Packet.destination = dst
            packet = Packet(src, dst, length)
            list_up_packet.append(packet)
            list_bi_packet.append(packet)
        else:
            packet = Packet(src, dst, length)
            tmp_time = float(_.sniff_timestamp)
            if  tmp_time - time > 1:
                li_bi = copy.copy(list_bi_packet)
                li_up = copy.copy(list_up_packet)
                li_down = copy.copy(list_down_packet)
                list_bi_burst.append(li_bi)
                list_up_burst.append(li_up)
                list_down_burst.append(li_down)
                list_bi_packet = []
                list_up_packet = []
                list_down_packet = []
                list_bi_packet.append(packet)
                if packet.len > 0:
                    list_up_packet.append(packet)
                else:
                    list_down_packet.append(packet)
                print("time: " + str(time))
            else:
                list_bi_packet.append(packet)
                if packet.len > 0:
                    list_up_packet.append(packet)
                else:
                    list_down_packet.append(packet)
            time = tmp_time
        idx += 1
    list_bi_burst.append(list_bi_packet)
    list_up_burst.append(list_up_packet)
    list_down_burst.append(list_down_packet)

    return list_up_burst, list_down_burst, list_bi_burst


if __name__=='__main__': main()