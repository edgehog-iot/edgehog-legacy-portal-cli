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
usage: epcli.py [-h] [-v] {binding,deregister,companies,os,releases} ...

Edgehog Portal Command Line Interface

positional arguments:
  {binding,deregister,companies,os,releases}
                        operators help
    binding             Binding parameters
    deregister          Deregister gateway
    companies           List all available companies
    os                  Operation on Operating system API
    releases            Operations on Releases API

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
```
---
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
---
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
---
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
---
###OS
Interface for the Operating Systems API
```
#: python epcli.py os --help
usage: epcli.py os [-h] {list,create} ...

positional arguments:
  {list,create}  OS operation help
    list         List Operating Systems
    create       Create new Operating System

optional arguments:
  -h, --help     show this help message and exit
```
####- List
Utility to list all operating systems registered on edgehog
```
#: python epcli.py os list --help
usage: epcli.py os list [-h] -u USER [-e {test,staging,production}]

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  User email
  -e {test,staging,production}, --environment {test,staging,production}
                        Set the base URI (default: staging)
```
 
####- Create
Utility for Operating System creation
```
#: python epcli.py os create --help
usage: epcli.py os create [-h] -u USER [-e {test,staging,production}] --name
                          NAME --description DESCRIPTION --url URL

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  User email
  -e {test,staging,production}, --environment {test,staging,production}
                        Set the base URI (default: staging)
  --name NAME           Operating System name
  --description DESCRIPTION
                        Operating System description
  --url URL             Operating System URL
```
---
### Releases
Interface for the Releases API
```
#: python epcli.py releases --help
usage: epcli.py releases [-h] {list,create} ...

positional arguments:
  {list,create}  Releases operation help
    list         List releases
    create       List releases

optional arguments:
  -h, --help     show this help message and exit
```

#### - List
Utility to list all releases of a single OS
```
#: python epcli.py releases list --help
usage: epcli.py releases list [-h] -u USER [-e {test,staging,production}]
                              --osid OSID

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  User email
  -e {test,staging,production}, --environment {test,staging,production}
                        Set the base URI (default: staging)
  --osid OSID           Id of Operating System associated to release
```

#### - Create
Utility to add a new release on a single operating system.
```
#: python epcli.py releases create --help
usage: epcli.py releases create [-h] -u USER [-e {test,staging,production}]
                                --osid OSID --version VERSION --changelog
                                CHANGELOG --deltasize DELTASIZE [--date DATE]

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  User email
  -e {test,staging,production}, --environment {test,staging,production}
                        Set the base URI (default: staging)
  --osid OSID           Id of Operating System associated to release
  --version VERSION     OS Version
  --changelog CHANGELOG
                        Os release changelog
  --deltasize DELTASIZE
                        Delta size in MB
  --date DATE           Release date (default: now)
```
---