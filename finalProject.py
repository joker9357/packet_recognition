import copy
import os
import pyshark

from packet_recognition.Packet import Packet




def append_burst(target, element):
    list = copy.copy(element)
    target.append(list)
    element.clear()


def append_packet(up_list, down_list, bi_list, packet):
    bi_list.append(packet)
    if packet.len > 0:
        up_list.append(packet)
    else:
        down_list.append(packet)


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
        # parse the packet
        sum += int(_.ip.len)
        length = float(_.captured_length)
        dst = str(_.layers[1].dst)
        src = str(_.layers[1].src)
        # the first packet, get the source ip and destination ip
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
            print(tmp_time)
            # print(tmp_time)
            # start a new burst
            if tmp_time - time > 0.1:
                # copy and append the previous burst
                append_burst(list_up_burst,list_up_packet)
                append_burst(list_down_burst, list_down_packet)
                append_burst(list_bi_burst, list_bi_packet)
                append_packet(list_up_packet, list_down_packet, list_bi_packet, packet)
                print("time: " + str(time))
            #     append the existing burst
            else:
                append_packet(list_up_packet, list_down_packet, list_bi_packet, packet)
            time = tmp_time
        idx += 1
    list_bi_burst.append(list_bi_packet)
    list_up_burst.append(list_up_packet)
    list_down_burst.append(list_down_packet)
    return list_up_burst, list_down_burst, list_bi_burst


def get_data(list_burst):
    for burst in list_burst:
        for list in burst:
            for i in range(len(list)):
                list[i] = list[i].len


def load_data(path):
    list_res = []
    for file in os.listdir(path):
        try:
            cap = pyshark.FileCapture(file)
            listburst = get_burst(cap)
        except:
            print("not a file")
        get_data(listburst)
        list_res.append(listburst)
    return list_res

def main():
    list_social = load_data('social')
    list_finance = load_data('finance')
    list_communication = load_data('communication')

    print("Total length of ip is "+str(sum))


if __name__=='__main__': main()
