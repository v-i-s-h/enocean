# -*- encoding: utf-8 -*-
from __future__ import print_function, unicode_literals, division, absolute_import

from enocean.protocol.packet import Packet
from enocean.protocol.constants import RORG


def test_temperature():
    ''' Tests RADIO message for EEP -profile 0xA5 0x02 0x05 '''
    status, buf, packet = Packet.parse_msg(bytearray([
        0x55,
        0x00, 0x0A, 0x07, 0x01,
        0xEB,
        0xA5, 0x00, 0x00, 0x55, 0x08, 0x01, 0x81, 0xB7, 0x44, 0x00,
        0x01, 0xFF, 0xFF, 0xFF, 0xFF, 0x2D, 0x00,
        0x75
    ]))
    assert packet.parse_eep(0x02, 0x05) == ['TMP']
    assert round(packet.parsed['TMP']['value'], 1) == 26.7
    assert packet.parsed['TMP']['raw_value'] == 85
    assert packet.learn is False
    assert packet.contains_eep is False
    assert packet.rorg is 0xA5
    assert packet.rorg is int(RORG.BS4)
    assert packet.rorg_func is 0x02
    assert packet.rorg_type is 0x05
    assert packet.status == 0x00
    assert packet.repeater_count == 0
    assert packet.sender == [0x01, 0x81, 0xB7, 0x44]
    assert packet.sender_hex == '01:81:B7:44'


def test_magnetic_switch():
    ''' Tests RADIO message for EEP -profile 0xD5 0x00 0x01 '''
    status, buf, packet = Packet.parse_msg(bytearray([
        0x55,
        0x00, 0x07, 0x07, 0x01,
        0x7A,
        0xD5, 0x08, 0x01, 0x82, 0x5D, 0xAB, 0x00,
        0x01, 0xFF, 0xFF, 0xFF, 0xFF, 0x36, 0x00,
        0x53
    ]))
    assert packet.parse_eep(0x00, 0x01) == ['CO']
    assert packet.parsed['CO']['value'] == 'open'
    assert packet.parsed['CO']['raw_value'] == 0
    assert packet.status == 0x00
    assert packet.repeater_count == 0

    status, buf, packet = Packet.parse_msg(bytearray([
        0x55,
        0x00, 0x07, 0x07, 0x01,
        0x7A,
        0xD5, 0x09, 0x01, 0x82, 0x5D, 0xAB, 0x00,
        0x01, 0xFF, 0xFF, 0xFF, 0xFF, 0x36, 0x00,
        0xC7
    ]))
    assert packet.parse_eep(0x00, 0x01) == ['CO']
    assert packet.parsed['CO']['value'] == 'closed'
    assert packet.parsed['CO']['raw_value'] == 1
    assert packet.learn is False
    assert packet.status == 0x00
    assert packet.repeater_count == 0


def test_switch():
    status, buf, packet = Packet.parse_msg(bytearray([
        0x55,
        0x00, 0x07, 0x07, 0x01,
        0x7A,
        0xF6, 0x50, 0x00, 0x29, 0x89, 0x79, 0x30,
        0x01, 0xFF, 0xFF, 0xFF, 0xFF, 0x37, 0x00,
        0x9D
    ]))
    assert sorted(packet.parse_eep(0x02, 0x02)) == ['EB', 'NU', 'R1', 'R2', 'SA', 'T21']
    assert packet.parsed['SA']['value'] == 'No 2nd action'
    assert packet.parsed['EB']['value'] == 'pressed'
    assert packet.parsed['R1']['value'] == 'Button BI'
    assert packet.parsed['T21']['value'] is True
    assert packet.parsed['NU']['value'] is True
    assert packet.learn is True
    assert packet.status == 0x30
    assert packet.repeater_count == 0

    status, buf, packet = Packet.parse_msg(bytearray([
        0x55,
        0x00, 0x07, 0x07, 0x01,
        0x7A,
        0xF6, 0x00, 0x00, 0x29, 0x89, 0x79, 0x20,
        0x02, 0xFF, 0xFF, 0xFF, 0xFF, 0x4A, 0x00,
        0x03
    ]))
    assert sorted(packet.parse_eep(0x02, 0x02)) == ['EB', 'NU', 'R1', 'R2', 'SA', 'T21']
    assert packet.parsed['SA']['value'] == 'No 2nd action'
    assert packet.parsed['EB']['value'] == 'released'
    assert packet.parsed['T21']['value'] is True
    assert packet.parsed['NU']['value'] is False
    assert packet.learn is True
    assert packet.status == 0x20
    assert packet.repeater_count == 0


def test_eep_parsing():
    status, buf, packet = Packet.parse_msg(bytearray([
        0x55,
        0x00, 0x0A, 0x07, 0x01,
        0xEB,
        0xA5, 0x08, 0x28, 0x46, 0x80, 0x01, 0x8A, 0x7B, 0x30, 0x00,
        0x01, 0xFF, 0xFF, 0xFF, 0xFF, 0x49, 0x00,
        0x26
    ]))
    assert packet.learn is True
    assert packet.contains_eep is True
    assert packet.rorg_func == 0x02
    assert packet.rorg_type == 0x05
    assert packet.status == 0x00
    assert packet.repeater_count == 0


def test_eep_remaining():
    # Magnetic switch -example
    status, buf, packet = Packet.parse_msg(bytearray([
        0x55,
        0x00, 0x07, 0x07, 0x01,
        0x7A,
        0xD5, 0x08, 0x01, 0x82, 0x5D, 0xAB, 0x00,
        0x01, 0xFF, 0xFF, 0xFF, 0xFF, 0x36, 0x00,
        0x53
    ]))
    assert packet.parse_eep(0x00, 0x01) == ['CO']

    # Temperature-example
    status, buf, packet = Packet.parse_msg(bytearray([
        0x55,
        0x00, 0x0A, 0x07, 0x01,
        0xEB,
        0xA5, 0x00, 0x00, 0x55, 0x08, 0x01, 0x81, 0xB7, 0x44, 0x00,
        0x01, 0xFF, 0xFF, 0xFF, 0xFF, 0x2D, 0x00,
        0x75
    ]))
    # If this fails, the data is retained from the last Packet parsing!
    assert packet.parse_eep(0x00, 0x01) == []
    # Once we have parse with the correct func and type, this should pass.
    assert packet.parse_eep(0x02, 0x05) == ['TMP']


def test_eep_direction():
    status, buf, packet = Packet.parse_msg(bytearray([
        0x55,
        0x00, 0x0A, 0x07, 0x01,
        0xEB,
        0xA5, 0x32, 0x20, 0x89, 0x00, 0xDE, 0xAD, 0xBE, 0xEF, 0x00,
        0x03, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x00,
        0x43
    ]))
    assert sorted(packet.parse_eep(0x20, 0x01, 1)) == ['ACO', 'BCAP', 'CCO', 'CV', 'DWO', 'ENIE', 'ES', 'FTS', 'SO', 'TMP']
    assert packet.parsed['CV']['value'] == 50
    assert sorted(packet.parse_eep(0x20, 0x01, 2)) == ['LFS', 'RCU', 'RIN', 'SB', 'SP', 'SPI', 'SPS', 'TMP', 'VC', 'VO']
    assert packet.parsed['SP']['value'] == 50


def test_vld():
    status, buf, p = Packet.parse_msg(bytearray([
        0x55,
        0x00, 0x09, 0x07, 0x01,
        0x56,
        0xD2, 0x04, 0x00, 0x64, 0x01, 0x94, 0xE3, 0xB9, 0x00,
        0x01, 0xFF, 0xFF, 0xFF, 0xFF, 0x40, 0x00,
        0xE4
    ]))
    assert p.rorg == RORG.VLD
    assert sorted(p.parse_eep(0x01, 0x01)) == ['EL', 'IO', 'LC', 'OC', 'OV', 'PF', 'PFD']

    assert p.parsed['EL']['raw_value'] == 0
    assert p.parsed['EL']['value'] == 'Error level 0: hardware OK'

    assert p.parsed['PF']['raw_value'] == 0
    assert p.parsed['PF']['value'] == 'Power Failure Detection disabled/not supported'

    assert p.parsed['PFD']['raw_value'] == 0
    assert p.parsed['PFD']['value'] == 'Power Failure Detection not detected/not supported/disabled'

    assert p.parsed['IO']['raw_value'] == 0
    assert p.parsed['IO']['value'] == 'Output channel 0 (to load)'

    assert p.parsed['OV']['raw_value'] == 100
    assert p.parsed['OV']['value'] == 'Output value 100% or ON'

    assert p.parsed['OC']['raw_value'] == 0
    assert p.parsed['OC']['value'] == 'Over current switch off: ready / not supported'

    assert p.parsed['LC']['raw_value'] == 0
    assert p.parsed['LC']['value'] == 'Local control disabled / not supported'

    status, buf, p = Packet.parse_msg(bytearray([
        0x55,
        0x00, 0x09, 0x07, 0x01,
        0x56,
        0xD2, 0x04, 0x00, 0x00, 0x01, 0x94, 0xE3, 0xB9, 0x00,
        0x01, 0xFF, 0xFF, 0xFF, 0xFF, 0x40, 0x00,
        0xBF
    ]))
    assert p.rorg == RORG.VLD
    assert sorted(p.parse_eep(0x01, 0x01)) == ['EL', 'IO', 'LC', 'OC', 'OV', 'PF', 'PFD']

    assert p.parsed['EL']['raw_value'] == 0
    assert p.parsed['EL']['value'] == 'Error level 0: hardware OK'

    assert p.parsed['PF']['raw_value'] == 0
    assert p.parsed['PF']['value'] == 'Power Failure Detection disabled/not supported'

    assert p.parsed['PFD']['raw_value'] == 0
    assert p.parsed['PFD']['value'] == 'Power Failure Detection not detected/not supported/disabled'

    assert p.parsed['IO']['raw_value'] == 0
    assert p.parsed['IO']['value'] == 'Output channel 0 (to load)'

    assert p.parsed['OV']['raw_value'] == 0
    assert p.parsed['OV']['value'] == 'Output value 0% or OFF'

    assert p.parsed['OC']['raw_value'] == 0
    assert p.parsed['OC']['value'] == 'Over current switch off: ready / not supported'

    assert p.parsed['LC']['raw_value'] == 0
    assert p.parsed['LC']['value'] == 'Local control disabled / not supported'
