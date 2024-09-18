import re
import argparse
import os

ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}(?:/\d{1,2})?\b')
domain_pattern = re.compile(r'(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}')

def remove_ansi_escape_codes(text):
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

parser = argparse.ArgumentParser(description = " Extract subdomains and IP address from file")
parser.add_argument("input_file", help="Path to input file")
parser.add_argument("output_file", help="Base file name for the output files (domain_ and ip_ will be prefixed)")

args = parser.parse_args()

unique_domains = set()
unique_ips = set()

with open(args.input_file, 'r') as infile:
    for line in infile:
        clean_line = remove_ansi_escape_codes(line)

        ips = ip_pattern.findall(clean_line)
        unique_ips.update(ips)

        domains = domain_pattern.findall(clean_line)
        unique_domains.update(domains)

domain_output_file = f"domains_{os.path.basename(args.output_file)}"
ip_output_file = f"ips_{os.path.basename(args.output_file)}"

with open(domain_output_file, 'w') as domainfile:
    for domain in sorted(unique_domains):
        domainfile.write(domain + '\n')

with open(ip_output_file, 'w') as ipfile:
    for ip in sorted(unique_ips):
        ipfile.write(ip + '\n')


print(f"Data Extraction complete Results saved in '{args.output_file}'.")
