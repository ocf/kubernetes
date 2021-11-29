import sys

import ocfkube
import click


@click.group()
def cli(debug):
    pass


@cli.command()
@click.option("--module", required=True, type=str)
def print(module):
    """Generate new manifests and print them to stdout"""
    click.echo(ocfkube.build(module, write=False))


@cli.command()
@click.option("-m", "--module", "module", required=False, type=str)
def write(module: str = None):
    """Write new manifests to the manifests directory"""
    if module != None:
        ocfkube.build(module, write=True)
    else:
        ocfkube.build_changed()
    click.echo("Wrote manifests!")


if __name__ == "__main__":
    cli()
