"""Entrypoint for search file exercise."""
import click
from exer_search_file.domain import Searcher, Loader
from exer_search_file.adapters.db_rank import DBRanking
from exer_search_file.adapters.file_loader import FileLoader
from exer_search_file.entrypoints.cli import CLI


adapter_db = DBRanking()
adapter_file_loader = FileLoader()
use_case_searcher = Searcher(adapter_db)
use_case_loader = Loader(adapter_db, adapter_file_loader)
adapter_cli = CLI(use_case_searcher, use_case_loader)


@click.command()
@click.argument('path_db', default='resources/files', required=True)
def main(path_db: str):
    """Main endpoint."""
    adapter_cli.start(path_db)
