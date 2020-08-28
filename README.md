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
usage: epcli [-h] [-v]
             {binding,deregister,companies,os,releases,models,gateways,devices,apps,files,oscampaign,appcampaign,filecampaign}
             ...

Edgehog Portal Command Line Interface

positional arguments:
  {binding,deregister,companies,os,releases,models,gateways,devices,apps,files,oscampaign,appcampaign,filecampaign}
                        operators help
    binding             Binding parameters
    deregister          Deregister gateway
    companies           List all available companies
    os                  Operation on Operating system API
    releases            Operations on Releases API
    models              List all available models
    gateways            List all available public gateways
    devices             list all available devices
    apps                list all available apps
    files               list all available files
    oscampaign          list all available os campaign
    appcampaign         list all available app campaign
    filecampaign        list all available file campaign

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
Interface for the deregister API 
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
### OS
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
---
### Model
Interface for the Model API
```
#:python epcli models --help
usage: epcli models [-h] {list} ...

positional arguments:
  {list}      Operations on models public API
    list      List models

optional arguments:
  -h, --help  show this help message and exit
```
#### - List
Utility to list all the models linked to the user
```
#: python epcli models list --help
usage: epcli models list [-h] -u USER [-p PWD] [-e {test,staging,production}]
                         [-f]

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  User email
  -p PWD, --pwd PWD     User password
  -e {test,staging,production}, --environment {test,staging,production}
                        Set the base URI (default: staging)
  -f, --force           Detached mode, does not show any warning if production
                        environment is selected
```
---
### Gateways
Interface for Gateways API
```
#: python epcli gateways --help
usage: epcli gateways [-h] {list,add} ...

positional arguments:
  {list,add}  Operations on gateways API
    list      List gateways
    add       Add a new gateway to user accounts company

optional arguments:
  -h, --help  show this help message and exit
```
#### - List
Utility to list all the gateways linked to the user
```
#: python epcli gateways list --help
usage: epcli gateways list [-h] [--unassociated [UNASSOCIATED]] -u USER
                           [-p PWD] [-e {test,staging,production}] [-f]

optional arguments:
  -h, --help            show this help message and exit
  --unassociated [UNASSOCIATED]
                        Inflate the zip file
  -u USER, --user USER  User email
  -p PWD, --pwd PWD     User password
  -e {test,staging,production}, --environment {test,staging,production}
                        Set the base URI (default: staging)
  -f, --force           Detached mode, does not show any warning if production
                        environment is selected
```
#### - Add
Utility to add a new gateway to user's company account
```
#:python epcli gateways add --help
usage: epcli gateways add [-h] -u USER [-p PWD] [-e {test,staging,production}]
                          [-f] [--serialnumber K... CODE]
                          [--registrationcode registration code]

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  User email
  -p PWD, --pwd PWD     User password
  -e {test,staging,production}, --environment {test,staging,production}
                        Set the base URI (default: staging)
  -f, --force           Detached mode, does not show any warning if production
                        environment is selected
  --serialnumber K... CODE
                        Gateway Serial Number
  --registrationcode registration code
                        Gateway Serial Number
```
---
### Files Models
Interface for File models API
```
#: python epcli files --help
usage: epcli files [-h] {list,add,versions,addversion} ...

positional arguments:
  {list,add,versions,addversion}
                        Operations on files API
    list                List all available file models
    add                 Add a new file model
    versions            List all available file versions
    addversion          Add a new file model

optional arguments:
  -h, --help            show this help message and exit
```
#### - List
Utility to list all file models linked to our user
```
#: python epcli files list --help
usage: epcli files list [-h] -u USER [-p PWD] [-e {test,staging,production}]
                        [-f] [--fileid [FILEID]]

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  User email
  -p PWD, --pwd PWD     User password
  -e {test,staging,production}, --environment {test,staging,production}
                        Set the base URI (default: staging)
  -f, --force           Detached mode, does not show any warning if production
                        environment is selected
  --fileid [FILEID]     File model ID
```
#### - Add
Utility to add a new file model
```
#: python epcli files add --help
usage: epcli files add [-h] -u USER [-p PWD] [-e {test,staging,production}]
                       [-f] [--name NAME] [--description DESCRIPTION]
                       [--file FILE] [--inflate [INFLATE]]
                       [--filedescription FILEDESCRIPTION]
                       [--remotepath REMOTEPATH] [--ack ACK]
                       [--tags [TAGS [TAGS ...]]]

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  User email
  -p PWD, --pwd PWD     User password
  -e {test,staging,production}, --environment {test,staging,production}
                        Set the base URI (default: staging)
  -f, --force           Detached mode, does not show any warning if production
                        environment is selected
  --name NAME           File model name
  --description DESCRIPTION
                        File model description
  --file FILE           Initial revision of the model
  --inflate [INFLATE]   Inflate the zip file
  --filedescription FILEDESCRIPTION
                        Description for initial revision file
  --remotepath REMOTEPATH
                        Destination path
  --ack ACK             Notify ack after download
  --tags [TAGS [TAGS ...]]
                        File model tags
```
#### - Verions
Utility to list file versions of a certain file model
```
#: python epcli files versions --help
usage: epcli files versions [-h] -u USER [-p PWD]
                            [-e {test,staging,production}] [-f]
                            [--fileid FILEID] [--versionid [VERSIONID]]

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  User email
  -p PWD, --pwd PWD     User password
  -e {test,staging,production}, --environment {test,staging,production}
                        Set the base URI (default: staging)
  -f, --force           Detached mode, does not show any warning if production
                        environment is selected
  --fileid FILEID       File model ID
  --versionid [VERSIONID]
                        File version ID 
```
#### - Add version
Utility to add a new file version
```
#: python epcli files addversion --help
usage: epcli files addversion [-h] -u USER [-p PWD]
                              [-e {test,staging,production}] [-f]
                              [--fileid FILEID] [--file FILE]
                              [--inflate [INFLATE]]
                              [--filedescription FILEDESCRIPTION]

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  User email
  -p PWD, --pwd PWD     User password
  -e {test,staging,production}, --environment {test,staging,production}
                        Set the base URI (default: staging)
  -f, --force           Detached mode, does not show any warning if production
                        environment is selected
  --fileid FILEID       File model ID
  --file FILE           Initial revision of the model
  --inflate [INFLATE]   Inflate the zip file
  --filedescription FILEDESCRIPTION
                        Description for initial revision file
```
---
### Applications
Interface for the Applications API
```
#: python epcli apps --help
usage: epcli apps [-h] {list,add} ...

positional arguments:
  {list,add}  Operations on apps API
    list      List all available apps
    add       Add a new app to your company

optional arguments:
  -h, --help  show this help message and exit
```
#### - List
Utility to list all the applications available to the user
```
#: python epcli apps list --help
usage: epcli apps list [-h] -u USER [-p PWD] [-e {test,staging,production}]
                       [-f] [--appid [APPID]]

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  User email
  -p PWD, --pwd PWD     User password
  -e {test,staging,production}, --environment {test,staging,production}
                        Set the base URI (default: staging)
  -f, --force           Detached mode, does not show any warning if production
                        environment is selected
  --appid [APPID]       Application ID
```
#### - Add
Utility to add a new application to the user
```
#: python epcli apps add --help
usage: epcli apps add [-h] -u USER [-p PWD] [-e {test,staging,production}]
                      [-f] [--name NAME] [--description DESCRIPTION]
                      [--configfile CONFIGFILE] [--start START]
                      [--tags [TAGS [TAGS ...]]]
                      [--gatewaymodels GATEWAYMODELS [GATEWAYMODELS ...]]

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  User email
  -p PWD, --pwd PWD     User password
  -e {test,staging,production}, --environment {test,staging,production}
                        Set the base URI (default: staging)
  -f, --force           Detached mode, does not show any warning if production
                        environment is selected
  --name NAME           Application name
  --description DESCRIPTION
                        Application description
  --configfile CONFIGFILE
                        Configuration file
  --start START         Start on Install or update
  --tags [TAGS [TAGS ...]]
                        Application tags
  --gatewaymodels GATEWAYMODELS [GATEWAYMODELS ...]
                        Gateway models IDs
```
---
### OS Update Campaign
Interface for the os-campaign API
```
#: python epcli oscampaign --help
usage: epcli oscampaign [-h] {list,add,start,cancel} ...

positional arguments:
  {list,add,start,cancel}
                        Operations on os campaign API
    list                List all available os campaign
    add                 Add new os campaign
    start               List all available os campaign
    cancel              List all available os campaign

optional arguments:
  -h, --help            show this help message and exit
```
#### - List
Utility to list all the OS update campaigns
```
python epcli oscampaign list --help
usage: epcli oscampaign list [-h] -u USER [-p PWD]
                             [-e {test,staging,production}] [-f]
                             [--campaignid [CAMPAIGNID]]

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  User email
  -p PWD, --pwd PWD     User password
  -e {test,staging,production}, --environment {test,staging,production}
                        Set the base URI (default: staging)
  -f, --force           Detached mode, does not show any warning if production
                        environment is selected
  --campaignid [CAMPAIGNID]
                        Device ID
```
#### - Add
Utility to add a new OS update campaign
```
python epcli oscampaign add --help
usage: epcli oscampaign add [-h] -u USER [-p PWD]
                            [-e {test,staging,production}] [-f] [--name NAME]
                            [--osid OSID] [--timeout [TIMEOUT]]
                            [--rollout [ROLLOUT]] [--tags [TAGS [TAGS ...]]]

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  User email
  -p PWD, --pwd PWD     User password
  -e {test,staging,production}, --environment {test,staging,production}
                        Set the base URI (default: staging)
  -f, --force           Detached mode, does not show any warning if production
                        environment is selected
  --name NAME           Os campaign name
  --osid OSID           OS to update id
  --timeout [TIMEOUT]   Timeout in minutes
  --rollout [ROLLOUT]   Rollout Rate
  --tags [TAGS [TAGS ...]]
                        Target devices tags
```
#### - Start
Utility to start am OS update campaign
```
python epcli oscampaign start --help
usage: epcli oscampaign start [-h] -u USER [-p PWD]
                              [-e {test,staging,production}] [-f]
                              [--campaignid CAMPAIGNID]

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  User email
  -p PWD, --pwd PWD     User password
  -e {test,staging,production}, --environment {test,staging,production}
                        Set the base URI (default: staging)
  -f, --force           Detached mode, does not show any warning if production
                        environment is selected
  --campaignid CAMPAIGNID
                        Device ID
```
#### - Cancel
Utility to cancel a started OS update campaign
```
python epcli oscampaign cancel --help
usage: epcli oscampaign cancel [-h] -u USER [-p PWD]
                               [-e {test,staging,production}] [-f]
                               [--campaignid CAMPAIGNID]

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  User email
  -p PWD, --pwd PWD     User password
  -e {test,staging,production}, --environment {test,staging,production}
                        Set the base URI (default: staging)
  -f, --force           Detached mode, does not show any warning if production
                        environment is selected
  --campaignid CAMPAIGNID
                        Device ID
```
---
### Applications Campaign
Interface for the application-campaign API
```
#: python epcli appcampaign --help
usage: epcli appcampaign [-h] {list,add,start,cancel} ...

positional arguments:
  {list,add,start,cancel}
                        Operations on app campaign API
    list                List all available app campaign
    add                 Add new app campaign
    start               List all available app campaign
    cancel              List all available app campaign

optional arguments:
  -h, --help            show this help message and exit
```
#### - List
Utility to list all the Application campaigns
```
#: python epcli appcampaign list --help
usage: epcli appcampaign list [-h] -u USER [-p PWD]
                              [-e {test,staging,production}] [-f]
                              [--campaignid [CAMPAIGNID]]

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  User email
  -p PWD, --pwd PWD     User password
  -e {test,staging,production}, --environment {test,staging,production}
                        Set the base URI (default: staging)
  -f, --force           Detached mode, does not show any warning if production
                        environment is selected
  --campaignid [CAMPAIGNID]
                        Device ID
```
#### - Add
Utility to add a new Application campaign
```
#: python epcli appcampaign add --help
usage: epcli appcampaign add [-h] -u USER [-p PWD]
                             [-e {test,staging,production}] [-f] [--name NAME]
                             [--appid APPID]
                             [--campaignop {install,update,install_update,start,stop}]
                             [--timeout [TIMEOUT]] [--rollout [ROLLOUT]]
                             [--tags [TAGS [TAGS ...]]]

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  User email
  -p PWD, --pwd PWD     User password
  -e {test,staging,production}, --environment {test,staging,production}
                        Set the base URI (default: staging)
  -f, --force           Detached mode, does not show any warning if production
                        environment is selected
  --name NAME           App campaign name
  --appid APPID         App to update id
  --campaignop {install,update,install_update,start,stop}
                        Action executed by the campaign
  --timeout [TIMEOUT]   Timeout in minutes
  --rollout [ROLLOUT]   Rollout Rate
  --tags [TAGS [TAGS ...]]
                        Target devices tags
```
#### - Start
Utility to start an Application campaign
```
#: python epcli appcampaign start --help
usage: epcli appcampaign start [-h] -u USER [-p PWD]
                               [-e {test,staging,production}] [-f]
                               [--campaignid CAMPAIGNID]

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  User email
  -p PWD, --pwd PWD     User password
  -e {test,staging,production}, --environment {test,staging,production}
                        Set the base URI (default: staging)
  -f, --force           Detached mode, does not show any warning if production
                        environment is selected
  --campaignid CAMPAIGNID
                        Device ID
```
#### - Cancel
Utility to cancel a started Application campaign
```
#: python epcli appcampaign cancel --help
usage: epcli appcampaign cancel [-h] -u USER [-p PWD]
                                [-e {test,staging,production}] [-f]
                                [--campaignid CAMPAIGNID]

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  User email
  -p PWD, --pwd PWD     User password
  -e {test,staging,production}, --environment {test,staging,production}
                        Set the base URI (default: staging)
  -f, --force           Detached mode, does not show any warning if production
                        environment is selected
  --campaignid CAMPAIGNID
                        Device ID
```
---
### File Campaign
Interface for the file-campaign API
```
#: python epcli filecampaign --help
usage: epcli filecampaign [-h] {list,add,start,cancel} ...

positional arguments:
  {list,add,start,cancel}
                        Operations on file campaign API
    list                List all available file campaign
    add                 Add new file campaign
    start               List all available file campaign
    cancel              List all available file campaign

optional arguments:
  -h, --help            show this help message and exit
```
#### - List
Utility to list all the File campaigns
```
#: python epcli filecampaign list --help
usage: epcli filecampaign list [-h] -u USER [-p PWD]
                               [-e {test,staging,production}] [-f]
                               [--campaignid [CAMPAIGNID]]

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  User email
  -p PWD, --pwd PWD     User password
  -e {test,staging,production}, --environment {test,staging,production}
                        Set the base URI (default: staging)
  -f, --force           Detached mode, does not show any warning if production
                        environment is selected
  --campaignid [CAMPAIGNID]
                        Device ID
```
#### - Add
Utility to add a new File campaign
```
#: python epcli filecampaign add --help
usage: epcli filecampaign add [-h] -u USER [-p PWD]
                              [-e {test,staging,production}] [-f]
                              [--name NAME] [--fileid FILEID]
                              [--campaignop {install,update,install_update}]
                              [--timeout [TIMEOUT]] [--rollout [ROLLOUT]]
                              [--tags [TAGS [TAGS ...]]]

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  User email
  -p PWD, --pwd PWD     User password
  -e {test,staging,production}, --environment {test,staging,production}
                        Set the base URI (default: staging)
  -f, --force           Detached mode, does not show any warning if production
                        environment is selected
  --name NAME           File campaign name
  --fileid FILEID       File to update id
  --campaignop {install,update,install_update}
                        Action executed by the campaign
  --timeout [TIMEOUT]   Timeout in minutes
  --rollout [ROLLOUT]   Rollout Rate
  --tags [TAGS [TAGS ...]]
                        Target devices tags
```
#### - Start
Utility to start a File campaign
```
#: python epcli filecampaign start --help
usage: epcli filecampaign start [-h] -u USER [-p PWD]
                                [-e {test,staging,production}] [-f]
                                [--campaignid CAMPAIGNID]

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  User email
  -p PWD, --pwd PWD     User password
  -e {test,staging,production}, --environment {test,staging,production}
                        Set the base URI (default: staging)
  -f, --force           Detached mode, does not show any warning if production
                        environment is selected
  --campaignid CAMPAIGNID
                        Device ID
```
#### - Cancel
Utility to cancel a started File campaign
```
#: python epcli filecampaign cancel --help
usage: epcli filecampaign cancel [-h] -u USER [-p PWD]
                                 [-e {test,staging,production}] [-f]
                                 [--campaignid CAMPAIGNID]

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  User email
  -p PWD, --pwd PWD     User password
  -e {test,staging,production}, --environment {test,staging,production}
                        Set the base URI (default: staging)
  -f, --force           Detached mode, does not show any warning if production
                        environment is selected
  --campaignid CAMPAIGNID
                        Device ID
```
