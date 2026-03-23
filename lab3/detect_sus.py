from entry_to_dict import entry_to_dict

def detect_sus(log, threshold, threshold_404=None, time_limit_seconds=None):
    if not isinstance(log, list):
        raise TypeError(f"Oczekiwano listy, otrzymano: {type(log).__name__}")
        
    ip_stats = {}
    for entry in log:
        entry_dict = entry_to_dict(entry)
        ip = entry_dict["ip"]
        if ip not in ip_stats:
            ip_stats[ip] = {
                "count": 0,
                "404_count": 0,
                "timestamps": []
            }
        
        ip_stats[ip]["count"] += 1
        if entry_dict["statusCode"] == 404:
            ip_stats[ip]["404_count"] += 1
        
        if entry_dict.get("ts"):
            ip_stats[ip]["timestamps"].append(entry_dict["ts"])
            
    suspicious_ips = set()
    
    for ip, stats in ip_stats.items():
        is_sus = False
        
        # 1. Sprawdzenie podstawowe: IP z dużą liczbą zapytań
        if stats["count"] >= threshold:
            is_sus = True
            
        # 2. Sprawdzenie opcjonalne: duża liczba błędów 404
        if not is_sus and threshold_404 is not None and stats["404_count"] >= threshold_404:
            is_sus = True
            
        # 3. Sprawdzenie opcjonalne: krótkie odstępy czasu 
        if not is_sus and time_limit_seconds is not None and stats["count"] > 1:
            sorted_ts = sorted(stats["timestamps"])
            if sorted_ts:
                total_duration = (sorted_ts[-1] - sorted_ts[0]).total_seconds()
                avg_interval = total_duration / (stats["count"] - 1)
                
                if avg_interval < time_limit_seconds:
                    is_sus = True
                
        if is_sus:
            suspicious_ips.add(ip)
            
    return list(suspicious_ips)

def test():
    from datetime import datetime
    
    testLogs = [
        (datetime(2026, 1, 1, 10, 0, 0), "uid1", "192.168.0.1", 80, "ip", 80, "GET", "host", "/A", 404),
        (datetime(2026, 1, 1, 10, 0, 1), "uid2", "192.168.0.1", 80, "ip", 80, "POST", "host", "/B", 404),
        (datetime(2026, 1, 1, 10, 0, 2), "uid3", "192.168.0.1", 80, "ip", 80, "GET", "host", "/C", 404),
        (datetime(2026, 1, 1, 10, 0, 3), "uid4", "10.0.0.5", 80, "ip", 80, "PUT", "host", "/D", 200),
        (datetime(2026, 1, 1, 10, 0, 4), "uid5", "10.0.0.5", 80, "ip", 80, "GET", "host", "/E", 200)
    ]
    
    print("Testy funkcji detect_sus")
    
    print("Test 1")
    res1 = detect_sus(testLogs, threshold=2, threshold_404=2)
    print(res1)
    
    print("Test 2")
    try:
        res2 = detect_sus("To nie jest lista logow", threshold=2)
        print(res2)
    except TypeError as e:
        print(e)
    
    print("Test 3")
    res3 = detect_sus([], threshold=2)
    print(res3)

if __name__ == "__main__":
    test()
