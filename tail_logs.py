import time
import os
import sys

LOG_FILE = "logs/app.log"

def tail_logs():
    """Continuously read and print new lines from the log file (like tail -f)."""
    if not os.path.exists(LOG_FILE):
        print(f"Log file {LOG_FILE} does not exist yet. Waiting...")
        while not os.path.exists(LOG_FILE):
            time.sleep(1)
            
    print(f"--- Tailing {LOG_FILE} ---")
    
    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        # Move the pointer to the end of the file so we only see new logs
        f.seek(0, os.SEEK_END)
        
        try:
            while True:
                line = f.readline()
                if not line:
                    time.sleep(0.1)  # Wait briefly for new data
                    continue
                sys.stdout.write(line)
                sys.stdout.flush()
        except KeyboardInterrupt:
            print("\n--- Stopped tailing logs ---")

if __name__ == "__main__":
    tail_logs()
