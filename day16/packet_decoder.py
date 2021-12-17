#!/usr/bin/env python

'''
--- Day 16: Packet Decoder ---
As you leave the cave and reach open waters, you receive a transmission from the Elves back
on the ship.

The transmission was sent using the Buoyancy Interchange Transmission System (BITS), a method
of packing numeric expressions into a binary sequence. Your submarine's computer has saved
the transmission in hexadecimal (your puzzle input).

The first step of decoding the message is to convert the hexadecimal representation into binary
. Each character of hexadecimal corresponds to four bits of binary data:

0 = 0000
1 = 0001
2 = 0010
3 = 0011
4 = 0100
5 = 0101
6 = 0110
7 = 0111
8 = 1000
9 = 1001
A = 1010
B = 1011
C = 1100
D = 1101
E = 1110
F = 1111
The BITS transmission contains a single packet at its outermost layer which itself contains
many other packets. The hexadecimal representation of this packet might encode a few extra
0 bits at the end; these are not part of the transmission and should be ignored.

Every packet begins with a standard header: the first three bits encode the packet version,
and the next three bits encode the packet type ID. These two values are numbers; all numbers
encoded in any packet are represented as binary with the most significant bit first. For example
, a version encoded as the binary sequence 100 represents the number 4.

Packets with type ID 4 represent a literal value. Literal value packets encode a single binary
number. To do this, the binary number is padded with leading zeroes until its length is a multiple
of four bits, and then it is broken into groups of four bits. Each group is prefixed by a 1
bit except the last group, which is prefixed by a 0 bit. These groups of five bits immediately
follow the packet header. For example, the hexadecimal string D2FE28 becomes:

110100101111111000101000
VVVTTTAAAAABBBBBCCCCC
Below each bit is a label indicating its purpose:

The three bits labeled V (110) are the packet version, 6.
The three bits labeled T (100) are the packet type ID, 4, which means the packet is a literal value.
The five bits labeled A (10111) start with a 1 (not the last group, keep reading) and contain
the first four bits of the number, 0111.
The five bits labeled B (11110) start with a 1 (not the last group, keep reading) and contain
four more bits of the number, 1110.
The five bits labeled C (00101) start with a 0 (last group, end of packet) and contain the
last four bits of the number, 0101.
The three unlabeled 0 bits at the end are extra due to the hexadecimal representation and should
be ignored.
So, this packet represents a literal value with binary representation 011111100101, which is
2021 in decimal.

Every other type of packet (any packet with a type ID other than 4) represent an operator that
performs some calculation on one or more sub-packets contained within. Right now, the specific
operations aren't important; focus on parsing the hierarchy of sub-packets.

An operator packet contains one or more packets. To indicate which subsequent binary data represents
its sub-packets, an operator packet can use one of two modes indicated by the bit immediately
after the packet header; this is called the length type ID:

If the length type ID is 0, then the next 15 bits are a number that represents the total length
in bits of the sub-packets contained by this packet.
If the length type ID is 1, then the next 11 bits are a number that represents the number of
sub-packets immediately contained by this packet.
Finally, after the length type ID bit and the 15-bit or 11-bit field, the sub-packets appear.

For example, here is an operator packet (hexadecimal string 38006F45291200) with length type
ID 0 that contains two sub-packets:

00111000000000000110111101000101001010010001001000000000
VVVTTTILLLLLLLLLLLLLLLAAAAAAAAAAABBBBBBBBBBBBBBBB
The three bits labeled V (001) are the packet version, 1.
The three bits labeled T (110) are the packet type ID, 6, which means the packet is an operator.
The bit labeled I (0) is the length type ID, which indicates that the length is a 15-bit number
representing the number of bits in the sub-packets.
The 15 bits labeled L (000000000011011) contain the length of the sub-packets in bits, 27.
The 11 bits labeled A contain the first sub-packet, a literal value representing the number 10.
The 16 bits labeled B contain the second sub-packet, a literal value representing the number 20.
After reading 11 and 16 bits of sub-packet data, the total length indicated in L (27) is reached
, and so parsing of this packet stops.

As another example, here is an operator packet (hexadecimal string EE00D40C823060) with length
type ID 1 that contains three sub-packets:

11101110000000001101010000001100100000100011000001100000
VVVTTTILLLLLLLLLLLAAAAAAAAAAABBBBBBBBBBBCCCCCCCCCCC
The three bits labeled V (111) are the packet version, 7.
The three bits labeled T (011) are the packet type ID, 3, which means the packet is an operator.
The bit labeled I (1) is the length type ID, which indicates that the length is a 11-bit number
representing the number of sub-packets.
The 11 bits labeled L (00000000011) contain the number of sub-packets, 3.
The 11 bits labeled A contain the first sub-packet, a literal value representing the number 1.
The 11 bits labeled B contain the second sub-packet, a literal value representing the number 2.
The 11 bits labeled C contain the third sub-packet, a literal value representing the number 3.
After reading 3 complete sub-packets, the number of sub-packets indicated in L (3) is reached
, and so parsing of this packet stops.

For now, parse the hierarchy of the packets throughout the transmission and add up all of the version numbers.

Here are a few more examples of hexadecimal-encoded transmissions:

8A004A801A8002F478 represents an operator packet (version 4) which contains an operator packet (version 1) which contains an operator packet (version 5) which contains a literal value (version 6); this packet has a version sum of 16.
620080001611562C8802118E34 represents an operator packet (version 3) which contains two sub-packets; each sub-packet is an operator packet that contains two literal values. This packet has a version sum of 12.
C0015000016115A2E0802F182340 has the same structure as the previous example, but the outermost packet uses a different length type ID. This packet has a version sum of 23.
A0016C880162017C3686B18A3D4780 is an operator packet that contains an operator packet that contains an operator packet that contains five literal values; it has a version sum of 31.
Decode the structure of your hexadecimal-encoded BITS transmission; what do you get if you add up the version numbers in all packets?

Your puzzle answer was 920.

--- Part Two ---
Now that you have the structure of your transmission decoded, you can calculate the value of the expression it represents.

Literal values (type ID 4) represent a single number as described above. The remaining type IDs are more interesting:

Packets with type ID 0 are sum packets - their value is the sum of the values of their sub-packets. If they only have a single sub-packet, their value is the value of the sub-packet.
Packets with type ID 1 are product packets - their value is the result of multiplying together the values of their sub-packets. If they only have a single sub-packet, their value is the value of the sub-packet.
Packets with type ID 2 are minimum packets - their value is the minimum of the values of their sub-packets.
Packets with type ID 3 are maximum packets - their value is the maximum of the values of their sub-packets.
Packets with type ID 5 are greater than packets - their value is 1 if the value of the first sub-packet is greater than the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.
Packets with type ID 6 are less than packets - their value is 1 if the value of the first sub-packet is less than the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.
Packets with type ID 7 are equal to packets - their value is 1 if the value of the first sub-packet is equal to the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.
Using these rules, you can now work out the value of the outermost packet in your BITS transmission.

For example:

C200B40A82 finds the sum of 1 and 2, resulting in the value 3.
04005AC33890 finds the product of 6 and 9, resulting in the value 54.
880086C3E88112 finds the minimum of 7, 8, and 9, resulting in the value 7.
CE00C43D881120 finds the maximum of 7, 8, and 9, resulting in the value 9.
D8005AC2A8F0 produces 1, because 5 is less than 15.
F600BC2D8F produces 0, because 5 is not greater than 15.
9C005AC2F8F0 produces 0, because 5 is not equal to 15.
9C0141080250320F1802104A08 produces 1, because 1 + 3 = 2 * 2.
What do you get if you evaluate the expression represented by your hexadecimal-encoded BITS
transmission?

Your puzzle answer was 10185143721112.

Both parts of this puzzle are complete! They provide two gold stars: **
'''

class BITS_Packet:

    LITERAL_TYPE = 4

    SUBPACKETS_LEN_IN_BITS = 15
    SUBPACKETS_LEN_IN_QUANTITY = 11

    # lentgh ID: bit in size
    LENTGH_ID_VALUES = {
            0: SUBPACKETS_LEN_IN_BITS,
            1: SUBPACKETS_LEN_IN_QUANTITY
            }

    def __init__(self):
        # these 2 values represent the header
        self.version       = None
        # literal or operator
        self.type_id       = None

        # used if the packet is a literal
        self.literal_value_bin = ''
        self.literal_value = 0

        # Lenght ID if the packet is operator
        self.lenght_subpacket_id = None

        # Len of the subpackets, this could be in bits if
        # self.lenght_id = 0 or number of packets if self.lenght_id = 1
        self.subpackets_len = None

        self.size = 0

        # internal subpackets for this packet
        self.sub_packets   = []

    def subpackets_to_decode(self):
        # return True if there are subpackets that has not been decoded
        if self.lenght_subpacket_id == BITS_Packet.SUBPACKETS_LEN_IN_QUANTITY:
            # The lentgh value indicates the number of subtasks
            return self.subpackets_len > len(self.sub_packets)
        elif self.lenght_subpacket_id == BITS_Packet.SUBPACKETS_LEN_IN_BITS:
            # The lentgh value indicates the size in bits of subpackets
            # 3+3+1+15 represents constants for all packets in this category
            # Version+Type+LenghtID+SUbpacketsSize
            return self.subpackets_len > self.size - (3+3+1+15)

    def get_value(self):
        # Get final value of the packet and subpackets
        # TODO override __min__ __max__ __add__ __radd__ __eq__ __neq__ __lt__
        # __le__ __gt__ __ge__ to use operands directly

        if self.type_id == 4:
            # literal type, return the value
            return self.literal_value

        if self.type_id == 0:
            # sum
            value = 0
            for p in self.sub_packets:
                value += p.get_value()
        elif self.type_id == 1:
            # product
            value = 1
            for p in self.sub_packets:
                value *= p.get_value()
        elif self.type_id == 2:
            # min
            value = float("inf")
            for p in self.sub_packets:
                v = p.get_value()
                if value > v:
                    value = v
        elif self.type_id == 3:
            # max
            value = float("-inf")
            for p in self.sub_packets:
                v = p.get_value()
                if value < v:
                    value = v
        elif self.type_id == 5:
            # greater than
            p1, p2 = self.sub_packets
            value = 1 if p1.get_value() > p2.get_value() else 0
        elif self.type_id == 6:
            # less than
            p1, p2 = self.sub_packets
            value = 1 if p1.get_value() < p2.get_value() else 0
        elif self.type_id == 7:
            # equal to
            p1, p2 = self.sub_packets
            value = 1 if p1.get_value() == p2.get_value() else 0
        return value

class BITS_Transmission:
    def __init__(self):
        self.total_versions = 0

    @staticmethod
    def __hex_to_bin(hex):
        # convert the hex into an integex
        return bin(int(hex, 16))[2:].zfill(4)


    def decode_message(self, transmission):
        transmission_list = []
        for v in transmission:
            transmission_list.append(v)
        transmission_list.reverse()
        p, _ = self.__decode_message(transmission_list, '')
        return p

    def __decode_message(self, transmission, unused_bits):
        # Decode a message and add all the packets into the self._packet
        # transmission is the input transmission as a list in reverse order

        # TODO use integers and bit operands instead of strings for better performance
        # TODO add exception clauses in else statements

        packet = BITS_Packet()

        while transmission or unused_bits:
            if transmission:
                # transmission list can be over but there might still be some
                # bits in the unused_bits
                val_hex = transmission.pop()

                # Get the hex value in bits, this is a single hex character
                # the output is a value between 0-15
                bin_value_str = BITS_Transmission.__hex_to_bin(val_hex)

                # Add the unused bits from the previous decoding
                bin_value_str = unused_bits + bin_value_str
                unused_bits = ''
            else:
                # no more bytes in the transmission, keep using the unused_bits
                bin_value_str = unused_bits

            if packet.version is None:
                # Version is not defined. The first 3 bits represent the version
                version = int(bin_value_str[:3], 2)
                self.total_versions += version
                packet.version = version
                packet.size += 3

                # Set the unused bits
                unused_bits = bin_value_str[3:]
            elif packet.type_id is None:
                # Version was set but type has not been set
                # The unsued bit | with the 2 bits of bin_value are used
                type_id = int(bin_value_str[:3], 2)
                packet.type_id = type_id
                packet.size += 3

                # Set the unused bits
                unused_bits = bin_value_str[3:]
            elif packet.type_id == BITS_Packet.LITERAL_TYPE:
                # There are no subpackets
                # Find the value of the literal and return teh packet

                end_literal = int(bin_value_str[0], 2)

                # This is the end of the literal
                if len(bin_value_str) < 5:
                    # not enouhg bits
                    unused_bits = bin_value_str[0:]
                    continue

                # Get the next 4 bits for the literal value
                packet.literal_value_bin += bin_value_str[1:5]
                unused_bits = bin_value_str[5:]
                packet.size += 5

                if end_literal == 0:
                    # last 4 bits of the literal value
                    packet.literal_value = int(packet.literal_value_bin, 2)
                    return packet, unused_bits

            elif packet.type_id != BITS_Packet.LITERAL_TYPE:
                # This is a operator packet, there are one or more
                # subpackets

                # Get the lentgh ID to know how to get the subtasks

                if packet.lenght_subpacket_id is None:
                    # the lenght_id is a single bit
                    lenght_id = int(bin_value_str[0], 2)
                    packet.size += 1
                    bin_value_str = bin_value_str[1:]
                    packet.lenght_subpacket_id = BITS_Packet.LENTGH_ID_VALUES[lenght_id]

                if len(bin_value_str) < packet.lenght_subpacket_id:
                    # Still not big enough
                    unused_bits = bin_value_str[0:]
                    continue

                # There are enough bits to read the subpackets
                packet.subpackets_len = int(bin_value_str[:packet.lenght_subpacket_id], 2)
                unused_bits = bin_value_str[packet.lenght_subpacket_id:]
                packet.size += packet.lenght_subpacket_id


                # Get all the subpackets of the current packet
                while packet.subpackets_to_decode():
                    p, u = self.__decode_message(transmission, unused_bits)
                    packet.sub_packets.append(p)
                    packet.size += p.size
                    unused_bits = u

                # Return after all subpackets are added
                return packet, unused_bits


        return packet, unused_bits


transmission = BITS_Transmission()

with open('input_data.txt', 'r') as f:
    line = f.readline()
    while line:
        line = line.strip()
        # message is a single line
        packet = transmission.decode_message(line)
        line = f.readline()

print(f"Sum of all versions {transmission.total_versions}")
print(f"Value of the packet {packet.get_value()}")
