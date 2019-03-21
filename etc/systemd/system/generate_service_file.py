import os
import argparse


def get_args():
    parser = argparse.ArgumentParser()
    # parser.add_argument('-q', '--quiet', action='store_true', help='Never print a char (except on crash)')
    # parser.add_argument('-v', '--verbose', action='count', default=0, help='Print some informative messages')
    parser.add_argument('-H', '--hostname', required=True, help='Name of host, e.g. host.example.org')
    parser.add_argument('-c', '--command', required=True, help='Name of management command, e.g. save_raw_http')
    parser.add_argument('-O', '--outfile', default='', nargs='?',
                        help='Output file name (if empty: hostname_command.service)')
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    fname = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'management_template.service')

    with open(fname, 'rt') as f:
        fdata = f.read()

    fdata = fdata.replace('host.example.org', args.hostname)
    fdata = fdata.replace('management_command_name', args.command)
    if args.outfile == '':
        print(fdata)
    else:
        if args.outfile is None:
            outfile = f'{args.hostname}_{args.command}.service'
        else:
            outfile = args.outfile
        with open(outfile, 'wt') as f:
            f.write(fdata)


if __name__ == '__main__':
    main()
