import yaml
from configparser import ConfigParser
from point import Point

class Database:
    __config_name = "config.ini"

    def __init__(self):
        self.config = ConfigParser()
        self.config.read(self.__config_name)

    def getMacAddress(self) -> "":
        return self.config['MAC_ADDRESSES']['MainMacAddress']
        #return self.config['MAC_ADDRESSES']['BackupMacAddress']

    def getAllDevices(self) -> []:
        my_config_parser_dict = {s:dict(self.config.items(s)) for s in self.config.sections()}
        devices = [yaml.safe_load(x) for x in list(my_config_parser_dict['DEVICES'].values())]
        return [ {'id':device['id'], 'position':Point(device['x'], device['y'])}
                 for device in devices ]

def main():
    print(Database().getMacAddress())
    print(Database().getAllDevices())

if __name__ == "__main__":
    main()
