import time
import gzip
import os
import matplotlib.pyplot as plt

# Configuration
line = "This is a sample line of text for testing. " * 10 + "\n"
repeats = 500_000

# Output files
file_normal = "filewriteoptimization/normal_demo.txt"
file_buffered = "filewriteoptimization/buffered_demo.txt"
file_gzip = "filewriteoptimization/compressed_demo.txt.gz"

# Write functions
# USED FOR QUICK SMALL WRITES AND IN LOW-DEMAND CASES. SIMPLE AND RELIABLE
def write_normal(): 
    with open(file_normal, "w") as f:
        for _ in range(repeats):
            f.write(line)

# USED FOR HIGH-FREQUENCY OR LARGE BATCH-WRITES AND CASES WHERE REDUCING DISK WRITE CALLS IMPROVE PERFORMANCE.
# SIMILAR PERFORMACNE TO NORMAL WRITE B/C PYTHON AND OS ALREADY BUFFER BY DEFAULT AND TEST DATA DOESN'T PUT ENOUGH STRESS.
def write_buffered():
    with open(file_buffered, "w", buffering=8192) as f:
        for _ in range(repeats):
            f.write(line)

# ARCHIVING LARGE LOGS, REPORTS, RAW DATA AND CASES WHERE READ SPEED > WRITE SPEED. 
def write_gzip():
    with gzip.open(file_gzip, "wt") as f:
        for _ in range(repeats):
            f.write(line)

# Time measurement
def measure_time(func):
    start = time.time()
    func()
    return round(time.time() - start, 2)

# Run and measure
time_normal = measure_time(write_normal)
time_buffered = measure_time(write_buffered)
time_gzip = measure_time(write_gzip)

# File size in KB
size_normal = os.path.getsize(file_normal) / 1024
size_buffered = os.path.getsize(file_buffered) / 1024
size_gzip = os.path.getsize(file_gzip) / 1024

# Prepare data
methods = ['Normal Write', 'Buffered Write', 'Gzip Compression']
times = [time_normal, time_buffered, time_gzip]
sizes = [size_normal, size_buffered, size_gzip]

# Plot side-by-side graphs
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Write time bar chart
ax1.bar(methods, times, color=['skyblue', 'orange', 'lightgreen'])
ax1.set_ylabel('Time (seconds)')
ax1.set_title('Write Time Comparison')
ax1.grid(axis='y')

# File size bar chart
ax2.bar(methods, sizes, color=['skyblue', 'orange', 'lightgreen'])
ax2.set_ylabel('File Size (KB)')
ax2.set_title('File Size Comparison')
ax2.grid(axis='y')

plt.suptitle('File Write Optimization Methods: Time vs. Size')
plt.tight_layout()
plt.show()
