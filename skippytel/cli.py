import os
# if os.geteuid() != 0:
#     exit("You need to have root privileges to run this script.\nPlease try again with 'sudo'. Exiting.")
import sys
import click

CONTEXT_SETTINGS = dict(auto_envvar_prefix="SKIPPYTEL")

class Environment:
    def __init__(self):
        self.verbose = False
        self.home = os.getcwd()

    def log(self, msg, *args):
        """Logs a message to stderr."""
        if args:
            msg %= args
        click.echo(msg, file=sys.stderr)

    def vlog(self, msg, *args):
        """Logs a message to stderr only if verbose is enabled."""
        if self.verbose:
            self.log(msg, *args)
    
    def matrix(self):
        pass


pass_environment = click.make_pass_decorator(Environment, ensure=True)
cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "commands"))


class SkippyTelCLI(click.MultiCommand):
    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith(".py") and filename.startswith("cmd_"):
                rv.append(filename[4:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            mod = __import__(f"skippytel.commands.cmd_{name}", None, None, ["cli"])
        except ImportError:
            return
        return mod.cli


@click.command(cls=SkippyTelCLI, context_settings=CONTEXT_SETTINGS)
@click.option(
    "--home",
    type=click.Path(exists=True, file_okay=False, resolve_path=True),
    help="Changes the folder to operate on.",
    )
@click.option("-v", "--verbose", 
    is_flag=True, 
    help="Enables verbose mode."
    )
@pass_environment
def cli(ctx, verbose, home):
    """SkippyTel - Microwormhole LoRa Manager"""
    ctx.verbose = verbose
    if home is not None:
        ctx.home = home

    ctx.vlog(click.style(f"home = {ctx.home}", fg="yellow"))
