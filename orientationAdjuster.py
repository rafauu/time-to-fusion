class OrientationAdjuster:
    def __init__(self, angleFromRequest: {}):
        self.angle = angleFromRequest['angle']

    def getAngle(self) -> float:
        calibratedAngle = self.angle - 28
        return calibratedAngle if calibratedAngle > -180 else calibratedAngle + 360

def main():
    print(OrientationAdjuster({'angle':7}).getAngle())

if __name__ == "__main__":
    main()
