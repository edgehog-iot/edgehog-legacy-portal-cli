import argparse
import getpass
import sys
import os

from ep_operations import *

# Base URIs

TEST_BASE_URI = "http://homestead.test"
STAGING_BASE_URI = "https://staging-eu.syntheticbrain.cloud"
PRODUCTION_BASE_URI = "https://edgehog.cloud"


def deregister(uri: str, user: str, password: str, hardware_id: str):
    print('[TBI] deregister')


def main():
    used_base_url = STAGING_BASE_URI

    try:
        parser = argparse.ArgumentParser(description='Edgehog Portal Command Line Interface')
        parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1')

        subparsers = parser.add_subparsers(help='operators help', dest='operation')
        subparsers.required = True

        # binding parser
        parser_binding = subparsers.add_parser('binding', help='Binding parameters')
        parser_binding.add_argument('-u', '--user', required=True, type=str, help='User email')
        parser_binding.add_argument('-e', '--environment', choices=['test', 'staging', 'production'],
                                    help='Set the base URI (default: staging)', )
        parser_binding.add_argument('--company', nargs='?', type=str, help='Company code')
        parser_binding.add_argument('--hardwareid', nargs='?', metavar='16 CHAR', type=str, help='Gateway CPU id')
        parser_binding.add_argument('--serialnumber', nargs='?', metavar='K... CODE', type=str,
                                    help='Gateway Serial Number')
        parser_binding.add_argument('-i', '--input', nargs='?', type=argparse.FileType('r'), const='./input.csv',
                                    default=None, help='Input CSV files containing values for the requested operation')
        parser_binding.add_argument('-o', '--output', nargs='?', type=argparse.FileType('w'), const='./output.json',
                                    default=None, help='Output files containing server responses')
        parser_binding.add_argument('--dryrun', help='Remove binding after insert', action='store_true')

        # deregister parser
        deregister_parser = subparsers.add_parser('deregister', help='Deregister gateway')
        deregister_parser.add_argument('-u', '--user', required=True, type=str, help='User email')
        deregister_parser.add_argument('-e', '--environment', choices=['test', 'staging', 'production'],
                                       help='Set the base URI (default: staging)')
        deregister_parser.add_argument('--hardwareid', nargs='?', metavar='16 CHAR', type=str, help='Gateway CPU id')
        deregister_parser.add_argument('-i', '--input', nargs='?', type=argparse.FileType('r'), const='./input.csv',
                                       default=None,
                                       help='Input CSV files containing values for the requested operation')
        deregister_parser.add_argument('-o', '--output', nargs='?', type=argparse.FileType('w'), const='./output.json',
                                       default=None, help='Output files containing server responses')

        # companies parser
        companies_parser = subparsers.add_parser('companies', help='List all available companies')
        companies_parser.add_argument('-u', '--user', required=True, type=str, help='User email')
        companies_parser.add_argument('-e', '--environment', choices=['test', 'staging', 'production'],
                                      help='Set the base URI (default: staging)')

        # os parser
        os_parser = subparsers.add_parser('os', help='Operation on Operating system API')
        os_subparsers = os_parser.add_subparsers(help='OS operation help', dest='action')
        os_subparsers.required = True

        # os list parser
        os_list_parser = os_subparsers.add_parser('list', help='List Operating Systems')
        os_list_parser.add_argument('-u', '--user', required=True, type=str, help='User email')
        os_list_parser.add_argument('-e', '--environment', choices=['test', 'staging', 'production'],
                                    help='Set the base URI (default: staging)')
        os_list_parser.add_argument('--codeid', type=str, help='Operating System\'s code associated to release')

        # os create parser
        os_create_parser = os_subparsers.add_parser('create', help='Create new Operating System')
        os_create_parser.add_argument('-u', '--user', required=True, type=str, help='User email')
        os_create_parser.add_argument('-e', '--environment', choices=['test', 'staging', 'production'],
                                      help='Set the base URI (default: staging)')
        os_create_parser.add_argument('--name', required=True, type=str, help='Operating System name')
        os_create_parser.add_argument('--description', required=True, type=str, help='Operating System description')
        os_create_parser.add_argument('--url', required=True, type=str, help='Operating System URL')

        # releases parser
        releases_parser = subparsers.add_parser('releases', help='Operations on Releases API')
        releases_subparsers = releases_parser.add_subparsers(help='Releases operation help', dest='action')
        releases_subparsers.required = True

        # release list parser
        releases_list_parser = releases_subparsers.add_parser('list', help='List releases')
        releases_list_parser.add_argument('-u', '--user', required=True, type=str, help='User email')
        releases_list_parser.add_argument('-e', '--environment', choices=['test', 'staging', 'production'],
                                          help='Set the base URI (default: staging)')
        releases_list_parser.add_argument('--osid', type=str, help='Operating System\'id associated to release')
        releases_list_parser.add_argument('--codeid', type=str, help='Operating System\'s code associated to release')

        # release create parser
        releases_create_parser = releases_subparsers.add_parser('create', help='List releases')
        releases_create_parser.add_argument('-u', '--user', required=True, type=str, help='User email')
        releases_create_parser.add_argument('-e', '--environment', choices=['test', 'staging', 'production'],
                                            help='Set the base URI (default: staging)')
        releases_create_parser.add_argument('--osid', type=str, help='Operating System\'id associated to release')
        releases_create_parser.add_argument('--codeid', type=str, help='Operating System\'code associated to release')
        releases_create_parser.add_argument('--version', required=True, type=str, help='OS Version')
        releases_create_parser.add_argument('--changelog', required=True, type=str, help='Os release changelog')
        releases_create_parser.add_argument('--deltasize', required=True, type=int, help='Delta size in MB')
        releases_create_parser.add_argument('--date', type=str, help='Release date (default: now)')

        args = parser.parse_args()

        user_password = ''

        if args.user:
            while len(user_password) < 1:
                user_password = getpass.getpass("{} - password: ".format(args.user))

        if args.environment == 'test':
            used_base_url = TEST_BASE_URI
        elif args.environment == 'production':
            confirm = input('\n'
                            '*******************************************\n'
                            '|                 ATTENTION               |\n'
                            '*******************************************\n'
                            '\n'
                            'Are you sure you want to work in production? [y/N]: ')
            if confirm != 'y':
                print('Please omit -p parameter')
                return
            used_base_url = PRODUCTION_BASE_URI

        if args.operation == 'binding':
            psm.binding(used_base_url, args.user, user_password, company=args.company, hardware_id=args.hardwareid,
                        gateway_serial_number=args.serialnumber, input_file=args.input,
                        output_file=args.output, dryrun=args.dryrun)
        elif args.operation == 'deregister':
            deregister(used_base_url, args.user, user_password, hardware_id=args.hardwareid)
        elif args.operation == 'companies':
            companies.get_companies(used_base_url, args.user, user_password)
        elif args.operation == 'os':
            if args.action == 'list':
                operating_systems.get_oses(used_base_url, args.user, user_password, code_id=args.codeid)
            elif args.action == 'create':
                operating_systems.create_os(used_base_url, args.user, user_password, name=args.name,
                                            description=args.description, repository_url=args.url)
        elif args.operation == 'releases':
            if args.action == 'list':
                operating_systems.get_releases(used_base_url, args.user, user_password, os_id=args.osid,
                                               code_id=args.codeid)
            elif args.action == 'create':
                operating_systems.create_releases(used_base_url, args.user, user_password, os_id=args.osid,
                                                  version=args.version, changelog=args.changelog,
                                                  delta_size=args.deltasize, release_date=args.date,
                                                  code_id=args.codeid)

    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


if __name__ == "__main__":
    main()
