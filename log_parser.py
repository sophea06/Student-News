#!/usr/bin/env python3
"""
Log Parser Script for Web Server Logs

This script parses Apache/Nginx style access logs and provides a summary
including request counts by status code, method, path, IP, and time range.
"""

import sys
import re
from collections import Counter, defaultdict
from datetime import datetime

# Regex pattern to match log lines
LOG_PATTERN = r'(\d+\.\d+\.\d+\.\d+) - - \[([^\]]+)\] "(\w+) ([^"]+) HTTP/[\d.]+" (\d+) -'

def parse_log_line(line):
    """Parse a single log line and return extracted data."""
    match = re.match(LOG_PATTERN, line.strip())
    if not match:
        return None

    ip, timestamp_str, method, path, status = match.groups()

    # Parse timestamp
    # Format: 08/Nov/2025 15:13:43
    try:
        timestamp = datetime.strptime(timestamp_str, '%d/%b/%Y %H:%M:%S')
    except ValueError:
        timestamp = None

    return {
        'ip': ip,
        'timestamp': timestamp,
        'method': method,
        'path': path,
        'status': int(status)
    }

def analyze_logs(log_lines):
    """Analyze the log lines and return summary statistics."""
    parsed_logs = []
    timestamps = []

    for line in log_lines:
        parsed = parse_log_line(line)
        if parsed:
            parsed_logs.append(parsed)
            if parsed['timestamp']:
                timestamps.append(parsed['timestamp'])

    if not parsed_logs:
        return None

    # Calculate statistics
    total_requests = len(parsed_logs)

    status_counts = Counter(log['status'] for log in parsed_logs)
    method_counts = Counter(log['method'] for log in parsed_logs)
    path_counts = Counter(log['path'] for log in parsed_logs)
    ip_counts = Counter(log['ip'] for log in parsed_logs)

    # Time range
    if timestamps:
        start_time = min(timestamps)
        end_time = max(timestamps)
        duration = end_time - start_time
    else:
        start_time = end_time = duration = None

    return {
        'total_requests': total_requests,
        'status_counts': dict(status_counts.most_common()),
        'method_counts': dict(method_counts.most_common()),
        'path_counts': dict(path_counts.most_common(10)),  # Top 10 paths
        'ip_counts': dict(ip_counts.most_common(5)),  # Top 5 IPs
        'start_time': start_time,
        'end_time': end_time,
        'duration': duration
    }

def print_summary(summary):
    """Print the log analysis summary."""
    if not summary:
        print("No valid log entries found.")
        return

    print("=== Web Server Log Analysis Summary ===")
    print(f"Total Requests: {summary['total_requests']}")
    print()

    print("Status Codes:")
    for status, count in summary['status_counts'].items():
        print(f"  {status}: {count}")
    print()

    print("HTTP Methods:")
    for method, count in summary['method_counts'].items():
        print(f"  {method}: {count}")
    print()

    print("Top 10 Requested Paths:")
    for path, count in summary['path_counts'].items():
        print(f"  {path}: {count}")
    print()

    print("Top 5 Client IPs:")
    for ip, count in summary['ip_counts'].items():
        print(f"  {ip}: {count}")
    print()

    if summary['start_time'] and summary['end_time']:
        print("Time Range:")
        print(f"  Start: {summary['start_time']}")
        print(f"  End: {summary['end_time']}")
        print(f"  Duration: {summary['duration']}")
    else:
        print("Time Range: Unable to parse timestamps")

def main():
    """Main function to run the log parser."""
    # Read from stdin or command line arguments
    if len(sys.argv) > 1:
        # Read from file
        try:
            with open(sys.argv[1], 'r') as f:
                log_lines = f.readlines()
        except FileNotFoundError:
            print(f"Error: File '{sys.argv[1]}' not found.")
            sys.exit(1)
    else:
        # Read from stdin
        log_lines = sys.stdin.readlines()

    summary = analyze_logs(log_lines)
    print_summary(summary)

if __name__ == "__main__":
    main()