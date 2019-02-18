from broker.endpoint import ForwardProvider


class FileDumpForward(ForwardProvider):
    description = 'Dump data to a file'

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        # self.name = 'FileDump'  # You may override automatic values here

    def forward_data(self, data):
        # Forward data to another location, here it means dumping it to a file
        with open('/tmp/filedump.txt', 'wt') as f:
            f.write(str(data))
        return True
