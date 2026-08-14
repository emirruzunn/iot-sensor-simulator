import random
from datetime import datetime

class SensorSimulator:
    def __init__(self, sensor_id: str):
        self.sensor_id = sensor_id
        self.battery = 100.0

    def read_temperature(self) -> float:
        return round(random.uniform(15.0, 35.0), 1)

    def read_humidity(self) -> float:
        return round(random.uniform(30.0, 90.0), 1)

    def read_battery(self) -> float:
        """
        Batarya seviyesini her çağrıda 0.1 ile 0.5 arasında rastgele azaltır.
        Değerin 0.0'ın altına düşmesini engeller.
        """
        decrease_amount = random.uniform(0.1, 0.5)
        
        # max(0.0, ...) sayesinde batarya sıfırın altına düşmez
        self.battery = max(0.0, round(self.battery - decrease_amount, 1))
        
        return self.battery

    def read_all(self) -> dict:
        return {
            "sensor_id": self.sensor_id,
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "temperature": self.read_temperature(),
            "humidity": self.read_humidity(),
            "battery": self.read_battery()
        }