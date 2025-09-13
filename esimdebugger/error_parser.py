

import re

def analyze_log(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        print("[✓] Log file loaded\n")
        for line in lines:
            if "unknown device" in line.lower():
                print("[!] Error Detected: Unknown component used.")
                print("    Suggestion: Check spelling or library for component mentioned.")
            elif "floating" in line.lower():
                node = re.search(r"Node (\w+)", line)
                if node:
                    print(f"[!] Warning: Node {node.group(1)} is floating.")
                    print("    Suggestion: Connect this node to a known voltage or ground.")
            elif "no such model" in line.lower():
                model = re.search(r"model (\w+)", line)
                if model:
                    print(f"[!] Error: Missing model '{model.group(1)}'.")
                    print(f"Suggestion: Add .model {model.group(1)} ... to the netlist.")
            elif "invalid parameter" in line.lower():
                comp = re.search(r"for (\w+)", line)
                if comp:
                    print(f"[!] Error: Invalid parameter for {comp.group(1)}.")
                    print("Suggestion: Check value and format of the parameters.")
            else:
                print(f"[-] Log Info: {line.strip()}")

def main():
    file_path = r"C:\Users\sneha\esimdebugger\sampledata\sampleerror.log"
    analyze_log(file_path)

if __name__ == "__main__":
    main()

