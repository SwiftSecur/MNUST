import argparse
import subprocess
import concurrent.futures
import os
import ipaddress
import pyfiglet

ascii_art = pyfiglet.figlet_format("MNUST")
print(ascii_art)
print('Multithreaded Nmap Up Scan Thing')

def parse_args():
    parser = argparse.ArgumentParser(description="Multithreaded Nmap Up Scan Thing.")
    parser.add_argument(
        "-i", "--input", required=True, help="Path to the target list file (one target per line or CIDR range)"
    )
    parser.add_argument(
        "-o", "--output", default="live_hosts.txt", help="Output file for live hosts (default: live_hosts.txt)"
    )
    parser.add_argument(
        "-t", "--threads", type=int, default=10, help="Number of threads to use (default: 10)"
    )
    return parser.parse_args()

def parse_targets(file_path):
    targets = []
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                # Check if the line is a CIDR range
                network = ipaddress.ip_network(line, strict=False)
                targets.extend([str(ip) for ip in network.hosts()])
            except ValueError:
                # Otherwise, treat it as a plain IP or domain
                targets.append(line)
    return targets

def nmap_scan(target):
    try:
        # Command for TCP and UDP scan
        command = [
            "nmap",
            "-sS",  # Stealth TCP scan
            "-sU",  # UDP scan
            "--top-ports", "1000",  # Top 1000 common ports
            "--open",  # Only show open ports
            "-n",  # Disable DNS resolution
            "-Pn",  # Skip host discovery
            "-v",  # Verbose mode for incremental output
            "--max-retries", "3",  # Increase retries to 3
            "--host-timeout", "30s",  # Timeout per target
            target
        ]

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        for line in iter(process.stdout.readline, ""):
            line = line.strip()
            print(f"[DEBUG] {line}")

            if "open" in line.lower():
                print(f"[LIVE] {target} (Open port found: {line})")
                process.kill()  
                return target

        process.wait() 
        print(f"[DEAD] {target} (No open ports)")
        return None

    except Exception as e:
        print(f"Error scanning {target}: {e}")
        return None

def main():
    args = parse_args()
    if not os.path.isfile(args.input):
        print(f"Error: Target file '{args.input}' not found.")
        return

    targets = parse_targets(args.input)

    total_targets = len(targets)
    print(f"Starting scans for {total_targets} targets with {args.threads} threads...")

    live_hosts = []

    # Multithreading shizzle
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
        future_to_target = {executor.submit(nmap_scan, target): target for target in targets}

        for i, future in enumerate(concurrent.futures.as_completed(future_to_target), 1):
            target = future_to_target[future]
            try:
                result = future.result()
                if result:
                    live_hosts.append(result)
            except Exception as e:
                print(f"Error scanning {target}: {e}")

            # Progress output
            print(f"Progress: {i}/{total_targets} ({(i/total_targets)*100:.2f}%)")

    # Output all the things
    with open(args.output, "w") as f:
        for host in live_hosts:
            f.write(f"{host}\n")

    print(f"Scan complete. Live hosts saved to '{args.output}'.")

if __name__ == "__main__":
    main()
