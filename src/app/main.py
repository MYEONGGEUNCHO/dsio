import click
from datetime import datetime

# cli group
from cli.olympic import main as olympic

@click.group()
def main():
    pass

@main.command()
def test():
    print(1)

main.add_command(olympic, 'olympic')

if __name__ == "__main__":
    main()