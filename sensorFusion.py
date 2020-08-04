from math import sin, cos, radians
from database import Database
from point import Point

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
                               Database().getAllDevices())))

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
                 Point(self.x + self.__R * cos(radians(self.angle - self.__scanAngle)),
                       self.y + self.__R * sin(radians(self.angle - self.__scanAngle))),
                 Point(self.x + self.__R * cos(radians(self.angle + self.__scanAngle)),
                       self.y + self.__R * sin(radians(self.angle + self.__scanAngle)))
               ]

def main():
    print(SensorFusion(45, 300, 200).retrieveViableDevices())

if __name__ == "__main__":
    main()
