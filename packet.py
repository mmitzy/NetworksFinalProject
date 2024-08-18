class Packet:
    def __init__(self, stream_id, seq_no, data):
        """
        Packet constractor.
        :param stream_id: in order to know to which stream this packet belong.
        :param seq_no: the sequence number of the packet (same in all other protocols).
        :param data: the data bytes from the file we are transferring
        """
        self.stream_id = stream_id
        self.seq_no = seq_no
        self.data = data


    def encode(self):
        """
        Encoding the packet's parameters into a string in order to send them together.
        :return: the encoded string
        """
        message = f"{self.stream_id},{self.seq_no},{self.data.decode('latin-1')}"
        return message.encode('latin-1')


    @staticmethod
    def decode(data):
        """
        Decoding the packet's parameters back to a Packet form.
        :param data: the string that represent the packet (the encoded packet).
        :return: the decoded packet.
        """
        parts = data.decode('latin-1').split(',')
        stream_id = int(parts[0])
        seq_no = int(parts[1])
        data = ','.join(parts[2:]).encode('latin-1')
        return Packet(stream_id, seq_no, data)