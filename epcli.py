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

    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


if __name__ == "__main__":
    main()
