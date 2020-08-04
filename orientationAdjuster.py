class OrientationAdjuster:
    def getAngle(self, angleFromRequest: {}) -> float:
        calibratedAngle = angleFromRequest['angle'] - 28
        return calibratedAngle if calibratedAngle > -180 else calibratedAngle + 360

def main():
    print(OrientationAdjuster().getAngle({'angle':7}))

if __name__ == "__main__":
    main()
