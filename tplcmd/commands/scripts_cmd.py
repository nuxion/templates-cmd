from tplcmd.commands.common import console
from tplcmd.base import TemplateBase, TemplateSpec
from rich import print_json
from rich.table import Table

import click

@click.group()
def scripts():
    """ render scripts """
    pass

@scripts.command()
@click.option("--origin", "-o", default=None, help="Where template is located")
@click.option("--context-from", "-c", default=None, help="Get or read context from")
@click.option("--dst", "-d", default=None, help="where it will be rendered")
@click.option("--value", "-v", default=None,  help="Values to render: k:v", multiple=True)

@click.option("--values-file", "-f", default=None,  help="Values to render: k:v", multiple=True)
@click.argument("name")
def render(name, origin, context_from, dst, value, values_file):
    
    tpl = TemplateBase(source=origin)
    ctx = {}
    for kv in value:
        k, v = kv.split(":")
        ctx[k] = v
    tpl.render(name, dst, ctx=ctx)
    

@scripts.command()
@click.option("--filename", "-f", default=None, required=True, help="Name of the file")
@click.option("--origin", "-o", default=None, help="Where template is located")
@click.option("--author", "-a", default=None, help="Author of the template")
@click.option("--desc", "-d", default=None, help="Description")
@click.option("--schema", "-s", default=None, help="Schema template")
@click.argument("name")
def write(filename, origin, author, desc, schema, name, schema):
    tpl = TemplateBase(source=origin)
    spec = TemplateSpec(name=name, filename=filename, origin=origin, kind=kind, author=author, description=desc) 
    tpl.write_spec(name, spec)
    print_json(data=spec.dict())

@scripts.command(name="list")
@click.option("--origin", "-o", default=None, required=False, help="Name of the file")
def list_templates(origin):
    tpl = TemplateBase(source=origin)
    table = Table(title=f"Templates from {tpl.origin}")
    table.add_column("Name")
    table.add_column("File")
    table.add_column("Author")
    table.add_column("Description", no_wrap=False)
    for _tpl in tpl.list():
        table.add_row(_tpl.name, _tpl.filename, str(_tpl.author), str(_tpl.description))
    console.print(table)

@scripts.command(name="describe")
@click.option("--origin", "-o", default=None, required=False, help="Name of the file")
@click.argument("name")
def list_templates(name, origin):
    tpl = TemplateBase(source=origin)
    data = tpl.describe(name)   
    print_json(data=data)
