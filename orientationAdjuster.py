class OrientationAdjuster:
    def __init__(self, angleFromRequest: {}):
        self.angle = angleFromRequest['angle']

    def getAngle(self) -> float:
        calibratedAngle = self.angle - 18
        return [calibratedAngle if calibratedAngle > -180 else calibratedAngle + 360]
