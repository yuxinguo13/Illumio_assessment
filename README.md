# Flow Log Parser

This program parses AWS VPC Flow Logs and maps each flow to a tag based on a lookup table.

## Description

The Flow Log Parser processes AWS VPC Flow Logs (default format, version 2) and matches destination port and protocol combinations against a lookup table to apply tags. It generates statistics on matched tags and port/protocol combinations.

## Assumptions

1. The program only supports default log format, not custom formats. Only version 2 of flow logs is supported.
2. The protocol in the lookup table is matched case-insensitively with the protocol number in the flow logs.
3. If a flow doesn't match any entry in the lookup table, it's counted as "Untagged".
5. The flow log fields are space-separated as shown in the example.
6. The dstport and protocol in the lookup table uniquely determine the tag. If there are duplicate entries, the last one will be used.

## Environment Requirements

- Python 3.8 or higher

No external libraries are required, only the Python standard library.

## Usage (after git clone the repository)
```
cd Illumio_assessment
python parse_log.py
```

## Code
`parse_log.py`: Main program to parse flow logs and generate output

## Input Files
1. **Flow Log File** `log_files.txt`: A text file containing AWS VPC Flow Log records in the default format.
   - Format: `<version> <account-id> <interface-id> <srcaddr> <dstaddr> <srcport> <dstport> <protocol> <packets> <bytes> <start> <end> <action> <log-status>`
   - Example: `2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 49153 6 25 20000 1620140761 1620140821 ACCEPT OK`

2. **Lookup Table File** `lookup_table.csv`: A CSV file with three columns: `dstport`, `protocol`, and `tag`.
   - Example lookup table:
     ```
     dstport,protocol,tag
     25,tcp,sv_P1
     443,tcp,sv_P2
     110,tcp,email
     ```

3. **Protocol Numbers File** `protocol_numbers.csv`: A CSV file containing IANA protocol numbers mapping.
   - This is used to convert numeric protocol identifiers (e.g., '6') to their names (e.g., 'tcp').
   - from https://www.iana.org/assignments/protocol-numbers/protocol-numbers-1.csv. 

## Output File

The program generates two output files.

1. **Tag Counts** `Tag_Counts.csv`: The number of flow log records matching each tag.
    ```
    Tag,Count
    Untagged,8
    sv_P2 ,1
    sv_P1 ,2
    email,3
    ```

2. **Port/Protocol Combination Counts** `Protocol_Combination_Counts.csv`: The number of occurrences of each port/protocol combination.
    ```
    Port,Protocol,Count
    49153,tcp,1
    49154,tcp,1
    49155,tcp,1
    49156,tcp,1
    ```

## Performance Justification

- The program uses dictionaries for O(1) lookups
- It processes files line-by-line to handle large files without memory issues


## Notes

- Protocol numbers are mapped to protocol names using the IANA protocol numbers registry.
- The matching between port/protocol in flow logs and the lookup table is case-insensitive.