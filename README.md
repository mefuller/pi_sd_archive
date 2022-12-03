# pi-sd-archive

A CLI for creating archival images of SD cards and writing those images anew,
particularly with the Raspberry Pi in mind.

## About 

This project provides a CLI to wrap `dd`, `tar`, and the [PiShrink](https://github.com/Drewsif/PiShrink) utility.

The common location of `/dev/mmcblk0` is provided as a default to minimize
typing.

Obviously there's a lot more that could be done right as the current version is
quite bare-bones - pull requests are welcome.

## Setup and Use

I'm in the middle of fixing up some things and upgrading a wheel.

For now, the following works:

```sh
sudo python cli.py -a -z -o kodi_20221203.img
```

Please test that this is still ok:

```
virtualenv env
source env/bin/activate
pip install -r requirements.txt
python -m app --help
```

## Packaging 

Update `setup.py` with your details and then run `python setup.py upload` to package for distribution on PyPi.

## Contributing

- Fork the project and clone locally.
- Create a new branch for what you're going to work on.
- Push to your origin repository.
- Create a new pull request in GitHub.
