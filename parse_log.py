import csv
from collections import defaultdict

def load_protocol_map():
    """Load protocol numbers mapping from CSV file."""
    protocol_map = dict()
    # from https://www.iana.org/assignments/protocol-numbers/protocol-numbers-1.csv
    with open("files/protocol-numbers.csv", 'r') as file:
        for line in file:
            fields = line.strip().split(',')
            # Only grab protocol number
            if len(fields) >= 2 and fields[0].strip().isdigit():
                protocol_number = fields[0].strip()
                protocol_name = fields[1].strip().lower()
                protocol_map[protocol_number] = protocol_name
    return protocol_map

def load_lookup_table():
    """Load the lookup table from CSV file."""
    lookup_table = {}
    with open("files/lookup_table.csv", 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            port = int(row['dstport'])
            # case insensitive
            protocol = row['protocol'].lower()
            tag = row['tag']
            lookup_table[(port, protocol)] = tag
    return lookup_table

def process_flow_logs(protocol_map, lookup_table):
    """Process flow logs and count tag and port/protocol occurrences."""
    tag_counter = defaultdict(int)
    port_protocol_counter = defaultdict(int)
    
    with open("files/log_files.txt", 'r') as file:
        for line in file:
            if not line.strip():
                continue
                
            fields = line.strip().split()
            
            # Only process version 2 default version
            if fields[0] != '2':
                continue
                
            dstport = int(fields[6])
            protocol_num = fields[7]
            protocol = protocol_map.get(protocol_num, protocol_num).lower()
            
            port_protocol_counter[(dstport, protocol)] += 1
            
            if (dstport, protocol) in lookup_table:
                tag = lookup_table[(dstport, protocol)]
                tag_counter[tag] += 1
            else:
                tag_counter["Untagged"] += 1
                
    return tag_counter, port_protocol_counter

def write_output(tag_counter, port_protocol_counter):
    """Write results to output file."""
    # Write tag counts
    with open("Tag_Counts.csv", 'w', newline='') as file:
        file.write("Tag,Count\n")
        for tag, count in tag_counter.items():
            file.write(f"{tag},{count}\n")
    
    # Write port/protocol combination counts
    with open("Protocol_Combination_Counts.csv", 'w', newline='') as file:
        file.write("Port,Protocol,Count\n")
        for (port, protocol), count in port_protocol_counter.items():
            file.write(f"{port},{protocol},{count}\n")

def main():
    protocol_map = load_protocol_map()
    lookup_table = load_lookup_table()
    tag_counter, port_protocol_counter = process_flow_logs(protocol_map, lookup_table)
    
    # Write results to output file
    write_output(tag_counter, port_protocol_counter)
    
    print("Tag Counts:", dict(tag_counter))
    print("Port_Protocol Counts:", dict(port_protocol_counter))

    
if __name__ == "__main__":
    main()