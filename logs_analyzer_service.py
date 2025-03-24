from collections import Counter
import json

def parse_log_line(line):
    try:
        parts = line.split(" - ", 3)  # using split since its quite easy to implement rather than regex
        timestamp = parts[0]
        service_name = parts[1]
        log_level = parts[2]
        message = parts[3]
        return {"timestamp": timestamp, "service_name": service_name, "log_level": log_level, "message": message}
    except IndexError:
        return None

def analyze_logs(file_path):
    log_levels = Counter()
    services = Counter()
    error_messages = Counter()

    with open(file_path, "r") as file:
        for line in file:
            log_entry = parse_log_line(line.strip())
            if log_entry:
                log_levels[log_entry["log_level"]] += 1
                services[log_entry["service_name"]] += 1
                if log_entry["log_level"] == "ERROR":
                    error_messages[log_entry["message"]] += 1
            else:
                print(f"Warning: Malformed log line - {line.strip()}")

    return log_levels, services, error_messages

def get_most_common_error(error_messages):
    if error_messages:
        return error_messages.most_common(1)[0]
    else:
        return None, 0

def filter_logs_by_time_range(file_path, start_time, end_time):
    filtered_logs =[]
    with open(file_path, "r") as file:
        for line in file:
            log_entry = parse_log_line(line.strip())
            if log_entry:
                if start_time <= log_entry["timestamp"] <= end_time:
                    filtered_logs.append(log_entry)
    return filtered_logs

if __name__ == "__main__":
    file_path = "app.log"
    log_levels, services, error_messages = analyze_logs(file_path)

    print("Log Level Summary:")
    for level, count in log_levels.items():
        print(f"{level}: {count}")

    print("\nService Summary:")
    for service, count in services.items():
        print(f"{service}: {count}")

    most_common_error, error_count = get_most_common_error(error_messages)
    if most_common_error:
        print("\nMost Common Error:")
        print(f"Message: {most_common_error}, Count: {error_count}")
    else:
        print("\nNo errors found.")

    start_time = "2023-03-01 08:15:20" # can make it generic, just for test cases
    end_time = "2023-03-01 08:30:00"
    filtered_logs = filter_logs_by_time_range(file_path, start_time, end_time)

    print("\nFiltered Logs (between 2023-03-01 08:15:20 and 2023-03-01 08:30:00):")
    for log in filtered_logs:
        print(log)