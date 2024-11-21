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
