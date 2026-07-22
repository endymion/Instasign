import json
import time
import os

mock_file = "/Users/ryan/Projects/WLED/usermods/online_lookup/mock_launch.json"

states = [
    # 1. 30 hours away (Normal brightness: 2%, Status: Go/Green)
    {
        "date": "Demo",
        "time": "T-30h",
        "name": "State 1: > 24h",
        "vehicle": "2% Bright",
        "status_id": 1,
        "net_unix_offset": 30 * 3600
    },
    # 2. 12 hours away (Brightness: 10%, Status: Go/Green)
    {
        "date": "Demo",
        "time": "T-12h",
        "name": "State 2: < 24h",
        "vehicle": "10% Bright",
        "status_id": 1,
        "net_unix_offset": 12 * 3600
    },
    # 3. 1.5 hours away (Brightness: 20%, Status: Go/Green)
    {
        "date": "Demo",
        "time": "T-90m",
        "name": "State 3: < 2h",
        "vehicle": "20% Bright",
        "status_id": 1,
        "net_unix_offset": int(1.5 * 3600)
    },
    # 4. 30 minutes away (Brightness: 100%, Status: Go/Green)
    {
        "date": "Demo",
        "time": "T-30m",
        "name": "State 4: < 1h",
        "vehicle": "100% Bright",
        "status_id": 1,
        "net_unix_offset": 30 * 60
    },
    # 5. On Hold (Brightness: 100%, Status: Hold/Yellow)
    {
        "date": "Demo",
        "time": "HOLD",
        "name": "State 5: Hold",
        "vehicle": "Yellow Txt",
        "status_id": 5,
        "net_unix_offset": 15 * 60
    },
    # 6. Failure (Brightness: 100%, Status: Fail/Red)
    {
        "date": "Demo",
        "time": "FAIL",
        "name": "State 6: Fail",
        "vehicle": "Red Txt",
        "status_id": 4,
        "net_unix_offset": 0
    }
]

print("Running WLED Usermod Demo... (Press Ctrl+C to stop)")
try:
    while True:
        for state in states:
            # Calculate actual timestamp
            actual_state = state.copy()
            actual_state["net_unix"] = int(time.time()) + state["net_unix_offset"]
            del actual_state["net_unix_offset"]
            
            with open(mock_file, "w") as f:
                json.dump(actual_state, f)
            
            print(f"Switched to: {state['name']} | Status: {state['status_id']} | Offset: {state['net_unix_offset']}s")
            
            # Since pageIntervalSeconds is 1, and there are 4 pages, wait 5 seconds per state
            # so the user can see all 4 pages scroll by for this state
            time.sleep(6)
except KeyboardInterrupt:
    print("\nDemo stopped.")
