# Edgehog Portal CLI

Command Line Interface for Edgehog device manager portal

## Requirements:
### Python:
**Python 3.6+**

## Dependencies:
Requests 2.22.0

### Install dependencies
`pip install -r requirements.txt`


## Usage
### General use
No use, just for help and version
```
#: python epcli --help
usage: epcli [-h] [-v] {binding,deregister,companies,os,releases} ...

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
Interface for the Companies API
```
#: python epcli companies --help
usage: epcli companies [-h] {list,getos,addos} ...

positional arguments:
  {list,getos,addos}  Operations on Companies API
    list              List companies
    getos             List companies
    addos             List companies

optional arguments:
  -h, --help          show this help message and exit
```

#### - List
Utility to list all available companies
```
#: python epcli companies list --help
usage: epcli companies list [-h] -u USER [-p PWD]
                            [-e {test,staging,production}] [-f]

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  User email
  -p PWD, --pwd PWD     User password
  -e {test,staging,production}, --environment {test,staging,production}
                        Set the base URI (default: staging)
  -f, --force           Detached mode, does not show any warning if production
                        environment is selected
```
#### - Get OS
Utility to list all operating systems bound to a company
```
python epcli companies getos --help
usage: epcli companies getos [-h] -u USER [-p PWD]
                             [-e {test,staging,production}] [-f] --companycode
                             COMPANYCODE

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  User email
  -p PWD, --pwd PWD     User password
  -e {test,staging,production}, --environment {test,staging,production}
                        Set the base URI (default: staging)
  -f, --force           Detached mode, does not show any warning if production
                        environment is selected
  --companycode COMPANYCODE
                        Company code
```
#### - Add OS
Utility to bind an operating system to a company
```
python epcli companies addos --help
usage: epcli companies addos [-h] -u USER [-p PWD]
                             [-e {test,staging,production}] [-f] --companycode
                             COMPANYCODE --oscode OSCODE

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  User email
  -p PWD, --pwd PWD     User password
  -e {test,staging,production}, --environment {test,staging,production}
                        Set the base URI (default: staging)
  -f, --force           Detached mode, does not show any warning if production
                        environment is selected
  --companycode COMPANYCODE
                        Company code
  --oscode OSCODE       Operating System code
```
---
### Binding
Utility to register the <hardwareId, serialNumber, company> tuple on the 
edgehog device manager portal.

```
#: python epcli binding --help
usage: epcli binding [-h] -u USER [-p PWD] [-e {test,staging,production}] [-f]
                     [--company [COMPANY]] [--hardwareid [16 CHAR]]
                     [--serialnumber [K... CODE]] [-i [INPUT]] [-o [OUTPUT]]
                     [--dryrun]

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  User email
  -p PWD, --pwd PWD     User password
  -e {test,staging,production}, --environment {test,staging,production}
                        Set the base URI (default: staging)
  -f, --force           Detached mode, does not show any warning if production
                        environment is selected
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
#: python epcli deregister --help
usage: epcli deregister [-h] -u USER [-p PWD] [-e {test,staging,production}]
                        [-f] [--hardwareid [16 CHAR]] [-i [INPUT]]
                        [-o [OUTPUT]]

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  User email
  -p PWD, --pwd PWD     User password
  -e {test,staging,production}, --environment {test,staging,production}
                        Set the base URI (default: staging)
  -f, --force           Detached mode, does not show any warning if production
                        environment is selected
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
#: python epcli os --help
usage: epcli os [-h] {list,create} ...

positional arguments:
  {list,create}  OS operation help
    list         List Operating Systems
    create       Create new Operating System

optional arguments:
  -h, --help     show this help message and exit
```
#### - List
Utility to list all operating systems registered on edgehog
```
#: python epcli os list --help
usage: epcli os list [-h] -u USER [-p PWD] [-e {test,staging,production}] [-f]
                     [--codeid CODEID]

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  User email
  -p PWD, --pwd PWD     User password
  -e {test,staging,production}, --environment {test,staging,production}
                        Set the base URI (default: staging)
  -f, --force           Detached mode, does not show any warning if production
                        environment is selected
  --codeid CODEID       Operating System's code associated to release
```
 
#### - Create
Utility for Operating System creation
```
#: python epcli os create --help
usage: epcli os create [-h] -u USER [-p PWD] [-e {test,staging,production}]
                       [-f] --codeid CODEID --name NAME --description
                       DESCRIPTION --url URL

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  User email
  -p PWD, --pwd PWD     User password
  -e {test,staging,production}, --environment {test,staging,production}
                        Set the base URI (default: staging)
  -f, --force           Detached mode, does not show any warning if production
                        environment is selected
  --codeid CODEID       Operating System code
  --name NAME           Operating System name
  --description DESCRIPTION
                        Operating System description
  --url URL             Operating System URL
```
---
### Releases
Interface for the Releases API
```
#: python epcli releases --help
usage: epcli releases [-h] {list,create,delete} ...

positional arguments:
  {list,create,delete}  Releases operation help
    list                List releases
    create              List releases
    delete              List releases

optional arguments:
  -h, --help            show this help message and exit
```

#### - List
Utility to list all releases of a single OS
```
#: python epcli releases list --help
usage: epcli releases list [-h] -u USER [-p PWD]
                           [-e {test,staging,production}] [-f] [--osid OSID]
                           [--codeid CODEID]

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  User email
  -p PWD, --pwd PWD     User password
  -e {test,staging,production}, --environment {test,staging,production}
                        Set the base URI (default: staging)
  -f, --force           Detached mode, does not show any warning if production
                        environment is selected
  --osid OSID           Operating System's id associated to release
  --codeid CODEID       Operating System's code associated to release
```

#### - Create
Utility to add a new release on a single operating system.
```
#: python epcli releases create --help
usage: epcli releases create [-h] -u USER [-p PWD]
                             [-e {test,staging,production}] [-f] [--osid OSID]
                             [--codeid CODEID] --version VERSION --changelog
                             CHANGELOG --deltasize DELTASIZE [--date DATE]
                             [--dryrun]

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  User email
  -p PWD, --pwd PWD     User password
  -e {test,staging,production}, --environment {test,staging,production}
                        Set the base URI (default: staging)
  -f, --force           Detached mode, does not show any warning if production
                        environment is selected
  --osid OSID           Operating System's id associated to release
  --codeid CODEID       Operating System's code associated to release
  --version VERSION     OS Version
  --changelog CHANGELOG
                        Os release changelog
  --deltasize DELTASIZE
                        Delta size in MB
  --date DATE           Release date (default: now)
  --dryrun              Remove the release after insert
```
---


#### - Delete
Utility to remove a release on a single operating system.
```
#: python epcli releases delete --help
usage: epcli releases delete [-h] -u USER [-p PWD]
                             [-e {test,staging,production}] [-f] [--osid OSID]
                             [--codeid CODEID] --releaseid RELEASEID

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  User email
  -p PWD, --pwd PWD     User password
  -e {test,staging,production}, --environment {test,staging,production}
                        Set the base URI (default: staging)
  -f, --force           Detached mode, does not show any warning if production
                        environment is selected
  --osid OSID           Operating System's id associated to release
  --codeid CODEID       Operating System's code associated to release
  --releaseid RELEASEID
                        Release's id
```