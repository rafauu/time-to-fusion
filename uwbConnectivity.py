import bluepy.btle
import bitstruct
import time
from database import Database

LOCATION_DATA_CONTENT_NAMES = [
    'Position only',
    'Distances only',
    'Position and distances']

NETWORK_NODE_SERVICE_UUID = '680c21d9-c946-4c1f-9c11-baa1c21329e7'
LOCATION_DATA_CHARACTERISTIC_UUID = '003bbdf2-c634-4b3d-ab56-7ec889b89a37'
AMOUNT_OF_BYTES_FOR_POSITION = 13
SHORT_LOCAL_NAME_TYPE_CODE = 8

class UwbConnectivity:
    def __init__(self, peripheral):
        self.peripheral = peripheral

    def getPositionFromTag(self) -> {}:
        try:
            node_service = self.peripheral.getServiceByUUID(NETWORK_NODE_SERVICE_UUID)
            parsedData = {}
            collectDataUntilPositionReceived = True
            while collectDataUntilPositionReceived:
                locationBytes = node_service.getCharacteristics(LOCATION_DATA_CHARACTERISTIC_UUID)[0].read()
                parsedData = self._parse_location_data_bytes(locationBytes)
                if parsedData['position_data']:
                    print(parsedData)
                    collectDataUntilPositionReceived = False
            return parsedData
        except (bluepy.btle.BTLEDisconnectError):
            print("Device disconnected")
            self._connectAfterTimeout()
        except ():
            print("Exception occured, restarting connection")
            self._disconnectAfterTimeout()
            self._connectAfterTimeout()

    def _connectAfterTimeout(self) -> None:
        time.sleep(1)
        self.peripheral.connect(Database().getMacAddress())

    def _disconnectAfterTimeout(self) -> None:
        time.sleep(1)
        self.peripheral.disconnect()

    def _parse_location_data_bytes(self, location_data_bytes) -> {}:
        if len(location_data_bytes) > 0:
            location_data_content = location_data_bytes[0]
            location_data_bytes = location_data_bytes[1:]
        else:
            location_data_content = None
    
        if (location_data_content == 0 or location_data_content == 2):
            if len(location_data_bytes) < AMOUNT_OF_BYTES_FOR_POSITION:
                raise ValueError('Location data content byte indicated position data but less than 13 bytes follow')
            position_data = bitstruct.unpack_dict(
                's32s32s32u8<',
                ['x', 'y', 'z', 'quality'],
                location_data_bytes[:AMOUNT_OF_BYTES_FOR_POSITION])
        else:
            position_data = None
    
        return {
            'location_data_content_name': LOCATION_DATA_CONTENT_NAMES[location_data_content] if location_data_content else None,
            'position_data': position_data}
    
def main():
    UwbConnectivity().getPositionFromTag()

if __name__ == "__main__":
    main()
