import unittest
import datetime
import os 
from logs_analyzer_service import parse_log_line,filter_logs_by_time_range 

class LogAnalyzerTests(unittest.TestCase):

    def test_parse_log_line_valid(self):
        line = "2023-03-01 08:15:27 - ServiceA - INFO - Started processing request #123"
        expected_timestamp = "2023-03-01 08:15:27" 
        parsed_log = parse_log_line(line)
        self.assertIsNotNone(parsed_log)  # Check if parsing was successful
        self.assertEqual(parsed_log["timestamp"], expected_timestamp)
        self.assertEqual(parsed_log["service_name"], "ServiceA")
        self.assertEqual(parsed_log["log_level"], "INFO")
        self.assertEqual(parsed_log["message"], "Started processing request #123")

    def test_parse_log_line_invalid(self):
        line = "Invalid log line"
        self.assertIsNone(parse_log_line(line))

    def test_filter_logs_by_time_range(self):
        # Create a dummy log file for testing
        test_log_path = "test_log.log"
        with open(test_log_path, "w") as f:
            f.write("2023-03-01 08:15:27 - ServiceA - INFO - Entry 1\n")
            f.write("2023-03-01 08:30:00 - ServiceB - ERROR - Entry 2\n")
            f.write("2023-03-01 09:00:00 - ServiceC - WARN - Entry 3\n")

        start_time = "2023-03-01 08:20:00"
        end_time = "2023-03-01 08:45:00"
        filtered_logs = filter_logs_by_time_range(test_log_path, start_time, end_time)
        self.assertEqual(len(filtered_logs), 1)
        # Check if the expected entry is present
        expected_entry_found = False
        for log in filtered_logs:
            if "Entry 2" in log["message"]:
                expected_entry_found = True
                break
        self.assertTrue(expected_entry_found)

        # Clean up the dummy log file
        os.remove(test_log_path)

if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)