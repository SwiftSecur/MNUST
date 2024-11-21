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

def nmap_scan(target, output_file):
    try:
        
        command = [
            "nmap",
            "-sS",  
            "-sU",  
            "--top-ports", "1000", 
            "--open",  
            "-n", 
            "-Pn",  
            "-T5", 
            "--max-retries", "0",  
            "--host-timeout", "5s",  
            target
        ]

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        for line in iter(process.stdout.readline, ""):
            line = line.strip()
            print(f"[DEBUG] {line}")  

            if "open" in line.lower():
                print(f"[LIVE] {target} (Open port found: {line})")
                with open(output_file, "a") as f:  # Append to the output file
                    f.write(f"{target}\n")
                process.kill()  # Stop the Nmap process as soon as an open port is found
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

    with open(args.output, "w") as f:
        f.write("")  # Clear the file contents

    # Multithreading shizzle
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
        future_to_target = {executor.submit(nmap_scan, target, args.output): target for target in targets}

        for i, future in enumerate(concurrent.futures.as_completed(future_to_target), 1):
            target = future_to_target[future]
            try:
                future.result()
            except Exception as e:
                print(f"Error scanning {target}: {e}")

            print(f"Progress: {i}/{total_targets} ({(i/total_targets)*100:.2f}%)")

    print(f"Scan complete. Live hosts saved to '{args.output}'.")

if __name__ == "__main__":
    main()
