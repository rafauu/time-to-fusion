import math
import configparser
import yaml

class Point():
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

class SensorFusion():
    __R = 500
    __scanAngle = 25

    def __init__(self, angle: float, x: float, y: float):
        self.angle = angle
        self.x = x
        self.y = y
        self.coordinates = self._calculateTriangleCoordinates()

    def retrieveViableDevices(self) -> []:
        return list(map(lambda x: x['id'],
                        filter(self._isDeviceInRange,
                               self._getAllDevices())))

    def _isDeviceInRange(self, device) -> bool:
        return abs(self._area(device["position"], self.coordinates[0], self.coordinates[1]) +
                   self._area(device["position"], self.coordinates[1], self.coordinates[2]) +
                   self._area(device["position"], self.coordinates[2], self.coordinates[0]) -
                   self._area(self.coordinates[0], self.coordinates[1], self.coordinates[2])) < 1.0

    def _area(self, A: Point, B: Point, C: Point) -> float:
        return abs(A.x * (B.y - C.y) + B.x * (C.y - A.y) + C.x * (A.y - B.y)) / 2.0

    def _calculateTriangleCoordinates(self) -> []:
        return [
                 Point(self.x,
                       self.y),
                 Point(self.x + self.__R * math.cos(math.radians(self.angle - self.__scanAngle)),
                       self.y + self.__R * math.sin(math.radians(self.angle - self.__scanAngle))),
                 Point(self.x + self.__R * math.cos(math.radians(self.angle + self.__scanAngle)),
                       self.y + self.__R * math.sin(math.radians(self.angle + self.__scanAngle)))
               ]

    def _getAllDevices(self) -> []:
        config = configparser.ConfigParser()
        config.read('config.ini')
        my_config_parser_dict = {s:dict(config.items(s)) for s in config.sections()}
        devices = [yaml.safe_load(x) for x in list(my_config_parser_dict['DEVICES'].values())]
        return [ {'id':device['id'], 'position':Point(device['x'], device['y'])}
                 for device in devices ]

def main():
    print(SensorFusion(45, 300, 200).retrieveViableDevices())

if __name__ == "__main__":
    main()
