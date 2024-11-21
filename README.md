# MNUST - Multithreaded Nmap Up Scan Tool

![MNUST Banner](https://via.placeholder.com/800x200?text=MNUST+-+Multithreaded+Nmap+Up+Scan+Tool)

**MNUST** (Multithreaded Nmap Up Scan Thing) is a Python tool designed to perform fast and efficient network sweeps using **Nmap**. It leverages multithreading to scan multiple targets in parallel and stops scanning individual hosts as soon as an open port is detected.

## Features

- 🚀 **Multithreaded Scanning**: Scans multiple targets concurrently for maximum efficiency.
- ⚡ **Quick Results**: Stops scanning a host as soon as an open port is detected.
- 📡 **Real-Time Feedback**: Uses Nmap’s `-v` (verbose) mode to process results in real time.
- 🎯 **Customisable**: Adjust the number of threads, input files, and output file location via CLI options.
- 📄 **Output to File**: Saves live hosts to a simple `.txt` file for further processing.

## Requirements

- **Python 3.6+**
- **Nmap** (installed and accessible in your PATH)
- Python libraries:
  - `pyfiglet`

Install the required Python libraries with:

```bash
pip install pyfiglet
```

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/mnust.git
   cd mnust
   ```

2. Ensure `nmap` is installed on your system. You can install it via your package manager:
   - **Ubuntu/Debian**:
     ```bash
     sudo apt install nmap
     ```
   - **CentOS/RHEL**:
     ```bash
     sudo yum install nmap
     ```
   - **MacOS**:
     ```bash
     brew install nmap
     ```

3. Install the required Python libraries:
   ```bash
   pip install pyfiglet
   ```

## Usage

Run the script with the following options:

```bash
python mnust.py -i <input_file> -o <output_file> -t <threads>
```

### Arguments:

- `-i, --input`  
  Path to the target list file (one target per line).  
  **Example**: `targets.txt`

- `-o, --output`  
  Output file for live hosts. Default: `live_hosts.txt`.

- `-t, --threads`  
  Number of threads to use for concurrent scans. Default: `10`.

### Example:

```bash
python mnust.py -i targets.txt -o live_hosts.txt -t 20
```

### Input File Format:

The input file should contain a list of targets (IP addresses or domain names), one per line:

```
192.168.1.1
192.168.1.2
example.com
```

### Output:

The script outputs live hosts (those with at least one open port) to the specified output file, e.g., `live_hosts.txt`:

```
192.168.1.1
example.com
```

## How It Works

1. Reads a list of targets from the input file.
2. Scans each target for the top 1000 TCP and UDP ports using **Nmap**.
3. Processes **Nmap's verbose output** in real-time to detect open ports.
4. Stops scanning a host as soon as an open port is found.
5. Saves live hosts to the specified output file.

## Sample Output

```plaintext
Multithreaded Nmap Up Scan Thing
Starting scans for 3 targets with 3 threads...
[DEBUG] Starting Nmap 7.93 ( https://nmap.org ) at 2024-11-21 12:45 GMT
[DEBUG] Nmap scan report for 192.168.1.1
[DEBUG] 22/tcp open ssh
[LIVE] 192.168.1.1 (Open port found: 22/tcp open ssh)
Progress: 1/3 (33.33%)
[DEBUG] Starting Nmap 7.93 ( https://nmap.org ) at 2024-11-21 12:45 GMT
[DEBUG] Nmap scan report for 192.168.1.2
[DEBUG] No open ports found
[DEAD] 192.168.1.2 (No open ports)
Progress: 2/3 (66.67%)
Scan complete. Live hosts saved to 'live_hosts.txt'.
```

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

🎉 Happy Scanning!
