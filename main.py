from email.policy import default

from Rss2Discord.cml import CML
from time import sleep
import click
import os


@click.command()
@click.option('--interval', type=click.INT, help='Interval between crawl; env INTERVAL or 60',
              default=os.environ.get('INTERVAL', 60))
@click.option('--memory-file', default='memory.msgpack', type=click.Path(False, True, False, True, True))
@click.option('--config', default='config.yaml', type=click.Path(True, True, False, True, True))
@click.option('--only-build-memory', is_flag=True)
@click.option('--verbose', '-v', is_flag=True)
def cli(interval: int, only_build_memory: bool = False, memory_file: str = 'memory.msgpack',
        config: str = 'config.yaml', verbose: bool = False):
    cml = CML(interval, verbose, config, memory_file)

    if only_build_memory:
        cml.build_mem_only()
        return

    while True:
        cml.do_crawl_and_post()
        sleep(5)
    pass


if __name__ == '__main__':
    cli()
    pass
