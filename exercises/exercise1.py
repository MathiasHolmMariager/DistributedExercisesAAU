from emulators.Device import Device
from emulators.Medium import Medium
from emulators.MessageStub import MessageStub
import random

class GossipMessage(MessageStub):
    def __init__(self, sender: int, destination: int, secrets):
        super().__init__(sender, destination)
        self.secrets = secrets

    def __str__(self):
        return f'{self.source} -> {self.destination} : {self.secrets}'

class Gossip(Device):
    def __init__(self, index: int, number_of_devices: int, medium: Medium):
        super().__init__(index, number_of_devices, medium)
        # Each device starts knowing only their own secret
        self._secrets = set([index])

    def run(self):
        # If the device already knows all secrets, it can stop
        if len(self._secrets) == self.number_of_devices():
            return
        # Choose a peer to communicate with
        peer = self.choose_peer()
        if peer is not None:
            self.send_message(peer)

    def choose_peer(self):
        # Scenario 1: Total Graph (choose any peer except self)
        return random.choice([i for i in range(self.number_of_devices()) if i != self.index()])

    def send_message(self, peer):
        # Send a message with all known secrets to the selected peer
        message = GossipMessage(self.index(), peer, self._secrets)
        self.medium().send(message)

    def receive_message(self, message):
        # Update secrets upon receiving the message
        new_secrets = message.secrets - self._secrets  # Get secrets we don't already know
        if new_secrets:  # If we received new secrets
            self._secrets.update(message.secrets)  # Add new secrets to our set
            print(f'Device {self.index()} received secrets {new_secrets} from Device {message.source}')
            # Once secrets are updated, the device should also send them forward to others
            self.run()  # Continue running and sharing updated secrets

    def print_result(self):
        # Print the final result showing which secrets the device knows
        print(f'Device {self.index()} knows secrets: {self._secrets}')

