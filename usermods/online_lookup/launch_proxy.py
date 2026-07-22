import datetime
import zoneinfo
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import json
import os
import time
from urllib.parse import urlparse, parse_qs
launch_library_base_url = "https://ll.thespacedevs.com/2.3.0"
kennedy_space_center_search_term = "Kennedy Space Center"
kennedy_space_center_country_code = "USA"
kennedy_space_center_timezone = zoneinfo.ZoneInfo("America/New_York")


def fetch_paginated_results(endpoint_url, query_params):
    combined_results = []
    next_url = endpoint_url
    while next_url:
        response = requests.get(next_url, params=query_params, timeout=10)
        response.raise_for_status()
        data = response.json()
        combined_results.extend(data.get("results", []))
        next_url = data.get("next")
        query_params = None
    return combined_results


def find_kennedy_space_center_location_id():
    locations_url = f"{launch_library_base_url}/locations/"
    search_params = {
        "search": kennedy_space_center_search_term,
        "country_code": kennedy_space_center_country_code,
        "limit": 100,
    }
    locations = fetch_paginated_results(locations_url, search_params)
    matching_locations = [
        location
        for location in locations
        if kennedy_space_center_search_term.lower()
        in location.get("name", "").lower()
    ]
    if not matching_locations:
        raise RuntimeError("Kennedy Space Center location not found in Launch Library 2")
    primary_location = matching_locations[0]
    return primary_location["id"], primary_location


def fetch_upcoming_launches_for_location(location_id, result_limit=50):
    upcoming_launches_url = f"{launch_library_base_url}/launches/upcoming/"
    query_params = {
        "location__ids": location_id,
        "limit": result_limit,
        "ordering": "net",
    }
    upcoming_launches = fetch_paginated_results(upcoming_launches_url, query_params)
    return upcoming_launches


def parse_launch_net_timestamp(launch_data):
    net_text = launch_data.get("net")
    if not net_text:
        return None
    try:
        net_datetime = datetime.datetime.fromisoformat(net_text.replace("Z", "+00:00"))
        return net_datetime
    except ValueError:
        return None


def choose_next_launch(launches):
    launches_with_net = [
        (launch, parse_launch_net_timestamp(launch))
        for launch in launches
    ]
    launches_with_net = [
        (launch, net_dt)
        for launch, net_dt in launches_with_net
        if net_dt is not None
    ]
    if not launches_with_net:
        return None
    launches_with_net.sort(key=lambda item: item[1])
    return launches_with_net[0][0]


def convert_net_to_local_time(net_datetime_utc):
    if net_datetime_utc.tzinfo is None:
        net_datetime_utc = net_datetime_utc.replace(tzinfo=datetime.timezone.utc)
    localized_time = net_datetime_utc.astimezone(kennedy_space_center_timezone)
    return localized_time


def build_next_kennedy_launch_summary():
    location_id, location_data = find_kennedy_space_center_location_id()
    upcoming_launches = fetch_upcoming_launches_for_location(location_id)
    next_launch = choose_next_launch(upcoming_launches)
    if not next_launch:
        return {
            "location": location_data,
            "next_launch": None,
            "note": "No upcoming launches found for Kennedy Space Center",
        }

    net_datetime_utc = parse_launch_net_timestamp(next_launch)
    net_datetime_local = (
        convert_net_to_local_time(net_datetime_utc)
        if net_datetime_utc is not None
        else None
    )

    return {
        "location": location_data,
        "next_launch": next_launch,
        "net_utc": net_datetime_utc,
        "net_local": net_datetime_local,
    }


class LaunchProxyHandler(BaseHTTPRequestHandler):
    _lock = threading.Lock()
    _CACHE_DURATION = 3600  # 1 hour
    _CACHE_FILE = "/Users/ryan/Projects/WLED/usermods/online_lookup/launch_cache.json"
    
    if os.path.exists(_CACHE_FILE):
        try:
            with open(_CACHE_FILE, "r") as f:
                _cached_response = json.load(f)
            _last_fetch_time = time.time()
        except:
            _cached_response = None
            _last_fetch_time = 0
    else:
        _cached_response = None
        _last_fetch_time = 0
        
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        from urllib.parse import urlparse, parse_qs
        parsed_url = urlparse(self.path)
        qs = parse_qs(parsed_url.query)
        if qs.get('mock', [''])[0] == '1':
            try:
                import os

                mock_path = os.path.join(os.path.dirname(__file__), "mock_launch.json")
                with open(mock_path, "r") as f:
                    response_data = json.load(f)
                    response_data["current_unix"] = int(time.time())
                self.wfile.write(json.dumps(response_data).encode('utf-8'))
                return
            except Exception as e:
                response_data = {
                    "date": "ERR", "time": "ERR", "name": "Mock Missing", 
                    "vehicle": "ERR", "status_id": 2, "net_unix": 0, "current_unix": int(time.time())
                }
                self.wfile.write(json.dumps(response_data).encode('utf-8'))
                return
        
        with self._lock:
            current_time = time.time()
            if LaunchProxyHandler._cached_response is None or (current_time - LaunchProxyHandler._last_fetch_time > LaunchProxyHandler._CACHE_DURATION):
                try:
                    summary = build_next_kennedy_launch_summary()
                    if summary["next_launch"] is None:
                        response_data = {
                            "date": "TBD",
                            "time": "TBD",
                            "name": "No launches",
                            "vehicle": "-",
                            "status_id": 2 # TBD
                        }
                    else:
                        launch_name = summary["next_launch"].get("name", "Unknown Launch")
                        status_id = summary["next_launch"].get("status", {}).get("id", 2)
                        net_local = summary["net_local"]
                        
                        if net_local:
                            date_str = net_local.strftime("%b %d")
                            time_str = net_local.strftime("%H:%M %Z")
                        else:
                            date_str = "TBD"
                            time_str = "TBD"
                            
                        # Try to abbreviate long names
                        if "|" in launch_name:
                            name_short = launch_name.split("|")[1].strip()
                        else:
                            name_short = launch_name

                        provider = summary["next_launch"].get("launch_service_provider", {}).get("name", "Unknown")
                        rocket = summary["next_launch"].get("rocket", {}).get("configuration", {}).get("name", "Unknown")
                        
                        if provider == "SpaceX" and "Falcon 9" in rocket:
                            vehicle = "SpaceX Falcon 9"
                        elif provider == "SpaceX" and "Falcon Heavy" in rocket:
                            vehicle = "SpX Falcon Heavy"
                        elif provider == "United Launch Alliance":
                            vehicle = "ULA " + rocket
                        elif provider == "Rocket Lab":
                            vehicle = "RL " + rocket
                        else:
                            vehicle = provider
                            if len(vehicle) + len(rocket) + 1 <= 16:
                                vehicle += " " + rocket
                                
                        if len(vehicle) > 16:
                            vehicle = vehicle[:16]

                        response_data = {
                            "date": date_str,
                            "time": time_str,
                            "name": name_short,
                            "vehicle": vehicle,
                            "status_id": status_id,
                            "net_unix": int(net_local.timestamp()) if net_local else 0
                        }
                    LaunchProxyHandler._cached_response = response_data
                    LaunchProxyHandler._last_fetch_time = current_time
                    
                    try:
                        with open(LaunchProxyHandler._CACHE_FILE, "w") as f:
                            json.dump(response_data, f)
                    except:
                        pass
                except Exception as e:
                    if LaunchProxyHandler._cached_response is not None:
                        pass # Serve stale dict
                    else:
                        if "429 Client Error" in str(e):
                            response_data = {
                                "date": "TBD",
                                "time": "TBD",
                                "name": "API Limit",
                                "vehicle": "API Limit",
                                "status_id": 2, # TBD
                                "net_unix": 0
                            }
                            LaunchProxyHandler._cached_response = response_data
                            LaunchProxyHandler._last_fetch_time = current_time
                            
                            # Save to disk
                            try:
                                with open(LaunchProxyHandler._CACHE_FILE, "w") as f:
                                    json.dump(response_data, f)
                            except:
                                pass
                        else:
                            response_data = {
                                "date": "ERR",
                                "time": "ERR",
                                "name": str(e)[:16],
                                "vehicle": "ERR",
                                "status_id": 4 # Fail
                            }
                            LaunchProxyHandler._cached_response = response_data
            else:
                pass # do nothing, we will use the dict below

        if LaunchProxyHandler._cached_response is not None:
            # Inject current time on every request
            LaunchProxyHandler._cached_response["current_unix"] = int(time.time())
            response_text = json.dumps(LaunchProxyHandler._cached_response)
        else:
            response_text = "{}"

        self.wfile.write(response_text.encode('utf-8'))


def ensure_cached_launch_data():
    """Populate LaunchProxyHandler cache (same path as HTTP GET)."""
    handler = LaunchProxyHandler
    with handler._lock:
        current_time = time.time()
        if handler._cached_response is not None and (
            current_time - handler._last_fetch_time <= handler._CACHE_DURATION
        ):
            handler._cached_response["current_unix"] = int(time.time())
            return handler._cached_response

        # Force refresh by instantiating GET logic via a lightweight call
        try:
            summary = build_next_kennedy_launch_summary()
            if summary["next_launch"] is None:
                response_data = {
                    "date": "TBD",
                    "time": "TBD",
                    "name": "No launches",
                    "vehicle": "-",
                    "status_id": 2,
                    "net_unix": 0,
                }
            else:
                launch = summary["next_launch"]
                launch_name = launch.get("name", "Unknown Launch")
                status_id = launch.get("status", {}).get("id", 2)
                net_local = summary["net_local"]
                if net_local:
                    date_str = net_local.strftime("%b %d")
                    time_str = net_local.strftime("%H:%M %Z")
                else:
                    date_str = "TBD"
                    time_str = "TBD"
                if "|" in launch_name:
                    name_short = launch_name.split("|")[1].strip()
                else:
                    name_short = launch_name
                provider = launch.get("launch_service_provider", {}).get("name", "Unknown")
                rocket = launch.get("rocket", {}).get("configuration", {}).get("name", "Unknown")
                if provider == "SpaceX" and "Falcon 9" in rocket:
                    vehicle = "SpaceX Falcon 9"
                elif provider == "SpaceX" and "Falcon Heavy" in rocket:
                    vehicle = "SpX Falcon Heavy"
                elif provider == "United Launch Alliance":
                    vehicle = "ULA " + rocket
                elif provider == "Rocket Lab":
                    vehicle = "RL " + rocket
                else:
                    vehicle = provider
                    if len(vehicle) + len(rocket) + 1 <= 16:
                        vehicle += " " + rocket
                if len(vehicle) > 16:
                    vehicle = vehicle[:16]
                response_data = {
                    "date": date_str,
                    "time": time_str,
                    "name": name_short,
                    "vehicle": vehicle,
                    "status_id": status_id,
                    "net_unix": int(net_local.timestamp()) if net_local else 0,
                }
            handler._cached_response = response_data
            handler._last_fetch_time = current_time
            try:
                with open(handler._CACHE_FILE, "w") as f:
                    json.dump(response_data, f)
            except Exception:
                pass
        except Exception as e:
            print(f"ensure_cached_launch_data failed: {e}")
            if handler._cached_response is None:
                return None

        handler._cached_response["current_unix"] = int(time.time())
        return handler._cached_response


def push_launch_to_wled(wled_base_url):
    """Push cached launch fields into WLED /json/state (works when ESP cannot pull)."""
    data = ensure_cached_launch_data()
    if not data:
        print("No launch data to push")
        return False
    payload = {
        "OnlineLookup": {
            "name": data.get("name", ""),
            "vehicle": data.get("vehicle", ""),
            "date": data.get("date", ""),
            "time": data.get("time", ""),
            "status_id": data.get("status_id", 2),
            "net_unix": data.get("net_unix", 0),
        }
    }
    url = wled_base_url.rstrip("/") + "/json/state"
    try:
        response = requests.post(url, json=payload, timeout=8)
        response.raise_for_status()
        print(f"Pushed {data.get('name')} to {url}")
        return True
    except Exception as e:
        print(f"Push to WLED failed: {e}")
        return False


def push_loop(wled_base_url, interval_seconds=60):
    while True:
        push_launch_to_wled(wled_base_url)
        time.sleep(interval_seconds)


def run_server(port=8080, wled_url=None, push_interval=60):
    if wled_url:
        thread = threading.Thread(
            target=push_loop,
            args=(wled_url, push_interval),
            daemon=True,
        )
        thread.start()
        print(f"Pushing launch data to {wled_url} every {push_interval}s")

    server_address = ("", port)
    httpd = HTTPServer(server_address, LaunchProxyHandler)
    print(f"Starting WLED Launch Proxy on port {port}...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down proxy...")
        httpd.server_close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="KSC launch proxy / WLED pusher")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument(
        "--wled",
        default=os.environ.get("WLED_URL", "http://192.168.1.112"),
        help="WLED base URL to push /json/state updates into",
    )
    parser.add_argument("--push-interval", type=int, default=60)
    parser.add_argument(
        "--push-once",
        action="store_true",
        help="Push once to WLED and exit (no HTTP server)",
    )
    args = parser.parse_args()

    if args.push_once:
        ok = push_launch_to_wled(args.wled)
        raise SystemExit(0 if ok else 1)

    run_server(port=args.port, wled_url=args.wled, push_interval=args.push_interval)
