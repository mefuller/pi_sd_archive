"""
pi_sd_archive: a command line utility to backup, clone, SD cards
Copyright (C) 2022  Mark E. Fuller (fuller@fedoraproject.org)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import sys
from argparse import ArgumentParser

# https://docs.python.org/3/library/argparse.html
# https://www.golinuxcloud.com/python-argparse/


def main():
    parser = ArgumentParser(prog="pi_sd_archive")

    # output toggling (generic)
    parser.add_argument(
        "-q", "--quiet", action="store_true", dest="quiet", help="Suppress Output"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_false", dest="quiet", help="Verbose Output"
    )

    # flags to set behavior
    parser.add_argument(
        "-a",
        "--archive",
        action="store_true",
        dest="create_archive",
        help="Create minimal archive of SD card",
        default=False,
    )
    parser.add_argument(
        "-w",
        "--write",
        action="store_true",
        dest="write_disk",
        help="Write a target archive to SD card",
        default=False,
    )
    parser.add_argument(
        "-z",
        "--zip",
        action="store_true",
        dest="img_zip",
        help="Flag for whether image should be compressed when archiving or decompressed before writing",
        default=True,
    )

    # variables
    parser.add_argument(
        "-i",
        "--infile",
        default="/dev/mmcblk0",
        help="Input file for operation",
        type=str,
    )
    parser.add_argument(
        "-o",
        "--outfile",
        default="./sd.img",
        help="Output file for operation",
        type=str,
    )

    args = parser.parse_args()

    print(
        """
    pi_sd_archive: a command line utility to backup, clone, SD cards
    Copyright (C) 2022  Mark E. Fuller (fuller@fedoraproject.org)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
    """
    )

    parser.print_help()

    # some sanity checks
    if args.infile == args.outfile:
        print("\nSource and destination files are the same. Exiting.")
        sys.exit(1)
    elif args.create_archive and args.write_disk:
        print("\nBoth archive and write options provided. Exiting.")
        sys.exit(1)

    #


if __name__ == "__main__":
    main()
