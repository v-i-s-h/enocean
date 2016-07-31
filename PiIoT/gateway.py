#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import traceback
import os, sys, inspect
import time
from pprint import pprint

# Add modules to path
libPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "./../"))
if libPath not in sys.path:
    sys.path.insert(0, libPath)

from enocean.consolelogger import init_logging
import enocean.utils
from enocean.communicators.serialcommunicator import SerialCommunicator
from enocean.protocol.packet import RadioPacket
from enocean.protocol.constants import PACKET, RORG

try:
    import queue
except ImportError:
    import Queue as queue


def assemble_radio_packet(transmitter_id):
    return RadioPacket.create(rorg=RORG.BS4, rorg_func=0x20, rorg_type=0x01,
                              sender=transmitter_id,
                              CV=50,
                              TMP=21.5,
                              ES='true')


# init_logging()
communicator = SerialCommunicator()
communicator.start()
print('The Base ID of your module is %s.' % enocean.utils.to_hex_string(communicator.base_id))

if communicator.base_id is not None:
    print('Sending example package.')
    communicator.send(assemble_radio_packet(communicator.base_id))

# endless loop receiving radio packets
while communicator.is_alive():
    try:
        # Loop to empty the queue...
        packet = communicator.receive.get(block=True, timeout=1)

        if packet.packet_type == PACKET.RADIO and packet.rorg == RORG.BS1:
            # parse packet with given FUNC and TYPE
            fields = packet.parse_eep( 0x00, 0x01 )
            print time.strftime("%Y-%m-%d %H:%M:%S    ",time.localtime(time.time())),
            if u'CO' in fields:
                print packet.parsed['CO']['description'], " ", packet.parsed['CO']['value']
            else:
                print "Unknown packet with ", fields
            # for k in packet.parse_eep(0x02, 0x05):
            #     print('%s: %s' % (k, packet.parsed[k]))
        if packet.packet_type == PACKET.RADIO and packet.rorg == RORG.BS4:
            fields = packet.parse_eep( 0x02, 0x05 )
            print time.strftime("%Y-%m-%d %H:%M:%S    ",time.localtime(time.time())),
            if u'TMP' in fields:
                print packet.parsed['TMP']['description'], " ", packet.parsed['TMP']['value']
            else:
                print "Unknown packet with ", fields
            # # alternatively you can select FUNC and TYPE explicitely
            # packet.select_eep(0x00, 0x01)
            # # parse it
            # packet.parse_eep()
            # # for k in packet.parsed:
            #     print('%s: %s' % (k, packet.parsed[k]))
        if packet.packet_type == PACKET.RADIO and packet.rorg == RORG.RPS:
            fields = packet.parse_eep( 0x02, 0x02 )
            print time.strftime("%Y-%m-%d %H:%M:%S    ",time.localtime(time.time())),
            if 'R1' in fields:
                print packet.parsed['R1']['value'], " ", packet.parsed['EB']['value']
            else:
                print "Unknown packet"
            
    except queue.Empty:
        continue
    except KeyboardInterrupt:
        break
    except Exception:
        traceback.print_exc(file=sys.stdout)
        break

if communicator.is_alive():
    communicator.stop()
