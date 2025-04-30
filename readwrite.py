import os
import time
import matplotlib.pyplot as plt

# File path for testing
file_path = "demo.txt"
write_file_path = "demo_write.txt"

def create_demo_file(file_path):
    with open(file_path, "w") as f:
        for i in range(200000):  # Create a large file to see performance differences
            f.write(f"Sample text\n")


# High level read using Python's built-in open and read functions
def high_level_file_read(file_path):
    start_time = time.time()
    with open(file_path, "r") as file:
        content = file.read()
    end_time = time.time()
    return end_time - start_time

# Lower level read using os module open and read functions
def low_level_file_read(file_path):
    filedescriptor = os.open(file_path, os.O_RDONLY)
    start_time = time.time()
    content = os.read(filedescriptor, os.path.getsize(file_path))
    os.close(filedescriptor)
    end_time = time.time()
    return end_time - start_time


# High level write using Python's built-in open and write functions
def high_level_file_write(write_file_path):
    start_time = time.time()
    with open(write_file_path, "w") as f:
        for i in range(10000):  # Writing data to file
            f.write(f"Sample text\n")
    end_time = time.time()
    return end_time - start_time

# Lower level write using os module open and write functions
def low_level_file_write(write_file_path):
    filedescriptor = os.open(write_file_path, os.O_WRONLY | os.O_CREAT)
    start_time = time.time()
    for i in range(10000):  # Writing data to file
        os.write(filedescriptor, f"Sample text\n".encode('utf-8'))
    os.close(filedescriptor)
    end_time = time.time()
    return end_time - start_time


def main():
    # Create the demo file
    create_demo_file(file_path)

    # Measure times for each operation
    times = [
        high_level_file_read(file_path),   # File read high-level
        low_level_file_read(file_path),    # File read low-level
        high_level_file_write(write_file_path), # File write high-level
        low_level_file_write(write_file_path)   # File write low-level
    ]

    methods = [
        'File Read (High-level)',
        'File Read (Lower-level)',
        'File Write (High-level)',
        'File Write (Lower-level)'
    ]

    # Plot the results
    plt.figure(figsize=(10, 6))
    plt.barh(methods, times, color=['green', 'red', 'green', 'red'])
    plt.title('High-level vs Lower-level File Read/Write Performance')
    plt.xlabel('Time (seconds)')
    plt.tight_layout()
    plt.show()

    # Output times
    for method, time_taken in zip(methods, times):
        print(f"{method}: {time_taken:.6f} seconds")

if __name__ == "__main__":
    main()
