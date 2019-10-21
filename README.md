# Edgehog Portal CLI

Command Line Interface for Edgehog device manager portal

## Dependencies:
### Python:
**Python 3.6+**
### Libraries:
Requests 2.22.0

`pip install requests==2.22.0`

## Usage
### General use
No use, just for help and version
```
#: python epcli.py --help
usage: epcli.py [-h] [-v] {binding,deregister,companies} ...

Edgehog Portal Command Line Interface

positional arguments:
  {binding,deregister,companies}
                        operators help
    binding             Binding parameters
    deregister          Deregister gateway
    companies           List all available companies

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
```
### Companies
Utility to list all available companies

```
#: python epcli.py companies --help
usage: epcli.py companies [-h] -u USER [-e {test,staging,production}]

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  User email
  -e {test,staging,production}, --environment {test,staging,production}
                        Set the base URI (default: staging)
```
### Binding
Utility to register the <hardwareId, serialNumber, company> tuple on the 
edgehog device manager portal.

```
#: python epcli.py binding --help
usage: epcli.py binding [-h] -u USER [-e {test,staging,production}]
                        [--company [COMPANY]] [--hardwareid [16 CHAR]]
                        [--serialnumber [K... CODE]] [-i [INPUT]]
                        [-o [OUTPUT]] [--dryrun]

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  User email
  -e {test,staging,production}, --environment {test,staging,production}
                        Set the base URI (default: staging)
  --company [COMPANY]   Company code
  --hardwareid [16 CHAR]
                        Gateway CPU id
  --serialnumber [K... CODE]
                        Gateway Serial Number
  -i [INPUT], --input [INPUT]
                        Input CSV files containing values for the requested
                        operation
  -o [OUTPUT], --output [OUTPUT]
                        Output files containing server responses
  --dryrun              Remove binding after insert
```

**N.B.**
The file provided with the --input option must be a CSV in the format
```
HARDWARE_ID, SERIAL_NUMBER[, COMPANY_ID]
```

### Deregister
Utility to deregister a gateway **[TBI]**

```
#: python epcli.py deregister --help
usage: epcli.py deregister [-h] -u USER [-e {test,staging,production}]
                           [--hardwareid [16 CHAR]] [-i [INPUT]] [-o [OUTPUT]]

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  User email
  -e {test,staging,production}, --environment {test,staging,production}
                        Set the base URI (default: staging)
  --hardwareid [16 CHAR]
                        Gateway CPU id
  -i [INPUT], --input [INPUT]
                        Input CSV files containing values for the requested
                        operation
  -o [OUTPUT], --output [OUTPUT]
                        Output files containing server responses
```