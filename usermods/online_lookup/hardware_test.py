import argparse
import json
import time
import urllib.request
import os

WLED_IP = "192.168.2.26"
MOCK_FILE = os.path.join(os.path.dirname(__file__), "mock_launch.json")

# 4 pages * 3s per page = 12s per cycle. 2 cycles = 24 seconds total hold time
PAGE_INTERVAL_SECONDS = 3
HOLD_TIME_SECONDS = 24

BASE_DATA = {
    "name": "SDA Tranche 1",
    "vehicle": "SpaceX Falcon 9",
    "date": "Jul 17",
    "time": "13:30 PDT",
}

SCENARIOS = {
    "normal": {
        "status_id": 1,
        "net_unix_offset": 30 * 3600, # 30 hours away (1% brightness)
    },
    "24h": {
        "status_id": 1,
        "net_unix_offset": 12 * 3600, # 12 hours away (2% brightness)
    },
    "2h": {
        "status_id": 1,
        "net_unix_offset": int(1.5 * 3600), # 1.5 hours away (5% brightness)
    },
    "1h": {
        "status_id": 1,
        "net_unix_offset": 30 * 60, # 30 minutes away (100% brightness)
    },
    "hold": {
        "status_id": 5, # Hold (Yellow)
        "net_unix_offset": 15 * 60, # 15 minutes away
    },
    "t_minus_1m": {
        "status_id": 1,
        "net_unix_offset": 60, # 1 minute away (locked to countdown)
    },
    "fail": {
        "status_id": 4, # Fail (Red)
        "net_unix_offset": 0, # 0 minutes away
    },
    "post_launch_1h": {
        "status_id": 3,
        "net_unix_offset": -30 * 60, # 30 minutes past launch (100% bright, ALL green)
    },
    "post_launch_2h": {
        "status_id": 3,
        "net_unix_offset": -2 * 3600, # 2 hours past launch (2% bright, default colors)
    }
}

def set_wled_config():
    # Make sure WLED pulls constantly (interval=0) and pages fast (3s)
    # The proxy will serve ?mock=1 data
    config_url = f"http://{WLED_IP}/json/cfg"
    payload = {
        "um": {
            "OnlineLookup": {
                "updateInterval_m": 0,
                "pageIntervalSeconds": PAGE_INTERVAL_SECONDS
            }
        }
    }
    try:
        req = urllib.request.Request(config_url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'}, method='POST')
        with urllib.request.urlopen(req, timeout=5) as response:
            response.read()
    except Exception as e:
        print(f"Failed to configure WLED: {e}")

def run_scenario(scenario_name):
    if scenario_name not in SCENARIOS:
        print(f"Unknown scenario: {scenario_name}")
        return
    
    scenario_cfg = SCENARIOS[scenario_name]
    mock_data = BASE_DATA.copy()
    mock_data["status_id"] = scenario_cfg["status_id"]
    mock_data["net_unix"] = int(time.time()) + scenario_cfg["net_unix_offset"]
    
    with open(MOCK_FILE, "w") as f:
        json.dump(mock_data, f)
        
    print(f"Activated scenario: {scenario_name} (Status: {mock_data['status_id']}, TTL: {scenario_cfg['net_unix_offset']}s)")

def main():
    parser = argparse.ArgumentParser(description="WLED Hardware-in-the-loop Test Runner")
    parser.add_argument("--scenario", type=str, help="Run a specific scenario indefinitely", choices=SCENARIOS.keys())
    parser.add_argument("--all", action="store_true", help="Run a sequence through all scenarios")
    args = parser.parse_args()
    
    if not args.scenario and not args.all:
        parser.print_help()
        return

    print("Configuring WLED for testing...")
    set_wled_config()
    
    if args.scenario:
        print("Press Ctrl+C to stop.")
        try:
            # Re-apply occasionally to keep relative offset fresh
            while True:
                run_scenario(args.scenario)
                time.sleep(10)
        except KeyboardInterrupt:
            print("\nTest stopped.")
    elif args.all:
        try:
            for scenario in SCENARIOS.keys():
                run_scenario(scenario)
                print(f"Waiting {HOLD_TIME_SECONDS}s (2 full cycles)...")
                time.sleep(HOLD_TIME_SECONDS)
        except KeyboardInterrupt:
            print("\nTest stopped.")
        print("Test sequence complete.")

if __name__ == "__main__":
    main()
