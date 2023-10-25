# import csv
#
# import click
#
# from . import app, db
# from .models import URLMap
#
#
# @app.cli.command('load_opinions')
# def load_urls_command():
#     with open('urls.csv', encoding='utf-8') as f:
#         reader = csv.DictReader(f)
#         counter = 0
#         for row in reader:
#             url = URLMap(**row)
#             db.session.add(url)
#             db.session.commit()
#             counter += 1
#     click.echo(f'Загружено: {counter}')
