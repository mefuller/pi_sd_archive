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
import subprocess
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
        default=False,
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
        default="/dev/mmcblk0",
        help="Output file for operation",
        type=str,
    )

    args = parser.parse_args()

    if not args.quiet:
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

        print(
            """
        This program will likely require being run with root ('sudo') permissions!'
        It relies on the 'dd' utility - please see its documentation for additional information on input and output file names/destinations.
        """
        )

        parser.print_help()

    # some sanity checks
    if args.infile == args.outfile:
        sys.exit("\nSource and destination files are the same. Exiting.")
    elif args.create_archive and args.write_disk:
        sys.exit("\nBoth archive and write options provided. Exiting.")

    # create archive
    if args.create_archive:
        # strip ".tar.gz" if provided
        subprocess.run(
            [
                "dd",
                "bs=4M",
                "conv=fsync",
                "status=progress",
                f"if={args.infile}",
                f"of={args.outfile.removesuffix('.tar.gz')}",
            ]
        )
        subprocess.run(
            ["./pi_shrink/pishrink.sh", f"{args.outfile.removesuffix('.tar.gz')}"]
        )
        if args.img_zip:
            # compress image to tar.gz
            try:
                subprocess.run(
                    [
                        "tar",
                        "-czf",
                        args.outfile,
                        f"{args.outfile.removesuffix('.tar.gz')}",
                    ]
                )
            except:
                sys.exit("\nError decompressing image. Is it tar.gz? Exiting.")

    # writing to disk
    elif args.write_disk:
        if args.img_zip:
            # decompress tar.gz
            try:
                subprocess.run(["tar", "-xzf", args.infile])
            except:
                sys.exit("\nError decompressing image. Is it tar.gz? Exiting.")

        # write image, dropping ".tar.gz" from name provided, if given
        subprocess.run(
            [
                "dd",
                "bs=4M",
                "conv=fsync",
                "status=progress",
                f"if={args.infile.removesuffix('.tar.gz')}",
                f"of={args.outfile}",
            ]
        )


if __name__ == "__main__":
    main()
