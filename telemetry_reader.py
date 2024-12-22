import json
from dataclasses import dataclass
from typing import Optional
import hashlib
import uuid
import time

@dataclass
class TelemetryData:
    sqm_id: str
    machine_id: str
    dev_device_id: str
    mac_machine_id: Optional[str] = None

class TelemetryReader:
    def __init__(self, json_path: str):
        """Initialize TelemetryReader with path to storage.json"""
        self.json_path = json_path
        self.json_data = self._load_json_data()  # Store complete JSON data
        self.telemetry_data = self._extract_telemetry_data()

    def _load_json_data(self) -> dict:
        """Load complete JSON file"""
        try:
            with open(self.json_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Could not find storage.json at {self.json_path}")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in storage.json")

    def _extract_telemetry_data(self) -> TelemetryData:
        """Extract telemetry data from loaded JSON"""
        return TelemetryData(
            sqm_id=self.json_data.get('telemetry.sqmId', ''),
            machine_id=self.json_data.get('telemetry.machineId', ''),
            dev_device_id=self.json_data.get('telemetry.devDeviceId', ''),
            mac_machine_id=self.json_data.get('telemetry.macMachineId', '')
        )

    def update_machine_id(self, new_hex: str) -> None:
        """Update machine ID in JSON file"""
        self.json_data['telemetry.machineId'] = new_hex
        try:
            with open(self.json_path, 'w') as file:
                json.dump(self.json_data, file, indent=4)
            # Update local telemetry data
            self.telemetry_data.machine_id = new_hex
        except Exception as e:
            raise Exception(f"Failed to update JSON file: {e}")

    def get_all_telemetry(self) -> TelemetryData:
        """Return all telemetry data"""
        return self.telemetry_data

    def get_machine_id(self) -> str:
        """Return machine ID"""
        return self.telemetry_data.machine_id

    def get_dev_device_id(self) -> str:
        """Return dev device ID"""
        return self.telemetry_data.dev_device_id

    def get_mac_machine_id(self) -> str:
        """Return MAC machine ID"""
        return self.telemetry_data.mac_machine_id

    def update_telemetry_ids(self) -> tuple[str, str]:
        """Generate and update both machine ID and mac machine ID"""
        # Generate first hex for machine ID
        timestamp1 = str(time.time()).encode()
        unique_id1 = str(uuid.uuid4()).encode()
        new_machine_id = hashlib.sha256(timestamp1 + unique_id1).hexdigest()

        # Generate second hex for mac machine ID (with slight delay to ensure difference)
        time.sleep(0.001)  # Tiny delay to ensure different timestamp
        timestamp2 = str(time.time()).encode()
        unique_id2 = str(uuid.uuid4()).encode()
        new_mac_machine_id = hashlib.sha256(timestamp2 + unique_id2).hexdigest()

        # Update both IDs in JSON
        self.json_data['telemetry.machineId'] = new_machine_id
        self.json_data['telemetry.macMachineId'] = new_mac_machine_id

        try:
            with open(self.json_path, 'w') as file:
                json.dump(self.json_data, file, indent=4)
            # Update local telemetry data
            self.telemetry_data.machine_id = new_machine_id
            self.telemetry_data.mac_machine_id = new_mac_machine_id
        except Exception as e:
            raise Exception(f"Failed to update JSON file: {e}")

        return new_machine_id, new_mac_machine_id

    def generate_stats(self) -> dict:
        """Generate statistics and update JSON with new hexes"""
        values = [
            self.telemetry_data.sqm_id,
            self.telemetry_data.machine_id,
            self.telemetry_data.dev_device_id,
            self.telemetry_data.mac_machine_id
        ]
        non_empty_count = sum(1 for v in values if v)

        # Update both machine IDs
        new_machine_id, new_mac_machine_id = self.update_telemetry_ids()

        return {
            "total_fields": len(values),
            "non_empty_fields": non_empty_count,
            "total_characters": sum(len(str(v)) for v in values),
            "new_machine_id": new_machine_id,
            "new_mac_machine_id": new_mac_machine_id,
            "hex_length": len(new_machine_id)
        }

def main():
    try:
        reader = TelemetryReader('./storage.json')

        print("Original Values:")
        print(f"Machine ID: {reader.get_machine_id()}")
        print(f"MAC Machine ID: {reader.get_mac_machine_id()}")

        print("\nGenerating new stats and updating JSON...")
        stats = reader.generate_stats()

        print("\nStats:")
        print(f"Total fields: {stats['total_fields']}")
        print(f"Non-empty fields: {stats['non_empty_fields']}")
        print(f"Total characters: {stats['total_characters']}")
        print(f"\nNew Values ({stats['hex_length']} chars each):")
        print(f"New Machine ID: {stats['new_machine_id']}")
        print(f"New MAC Machine ID: {stats['new_mac_machine_id']}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
