import json
import glob
import os
from typing import TypeVar, Generic, Optional, Dict, List, Any
from abc import ABC, abstractmethod
from pydantic import BaseModel
from tplcmd.render import render_to_file, get_package_dir
from tplcmd import utils

T = TypeVar("T")

class DefaultParams(BaseModel):
    ctx: Dict[str, Any]

class DockerParams(BaseModel):
    image: str
    registry: Optional[str] = None

class DockerTemplate(TemplateSpec):
    values: DockerParams


class TemplateFile:
    filename: str
    dst: str

class TemplateSpec(BaseModel):
    name: str
    filename: str
    version: str = "v1"
    manager: str = "tplcmd.base.TemplateBase"
    schema: Optional[str] = "tplcmd.base.Defaultparams"
    origin: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None


class TemplateBase:

    def __init__(self, source: str = None):
        self._source = source or f"{get_package_dir('tplcmd')}/templates/"

    # def get_path(self) -> str:
    #     if self._group:
    #         return f"{self._source}/{group}"
    #     else:
    #         return self._source
    #
    @property
    def origin(self) -> str:
        return self._source
        
    def _open(self, fullpath) -> TemplateSpec:
        with open(fullpath, "r") as f:
            data = json.loads(f.read())
            tpl = TemplateSpec(**data)
        return tpl

    def open_spec(self, name) -> TemplateSpec:
        fullpath = f"{self._source}/{name}.spec.json"
        return self._open(fullpath)

    def write_spec(self, name: str, tpl: TemplateSpec):
        if not tpl.origin:
            tpl.origin = self._source
        with open(f"{self._source}/{name}.spec.json", "w") as f:
            f.write(json.dumps(tpl.dict()))

        
    def render(self, name: str, dst: str, ctx_dict: Dict[str, Any]):
        spec = self.open_spec(name)
        if spec.schema:
            B: BaseModel = get_class(spec.schema)
            _valid = B(**ctx_dict)
        render_to_file(spec.filename, dst=dst, env=os.environ, ctx=ctx_dict,
                       templates_dir=self._source)


    def list(self) -> List[TemplateSpec]:
        tpls = [ self._open(_tpl)
                 for _tpl in glob.glob(f"{self._source}*.spec.json")]
        return tpls

    def describe(self, name) -> Dict[str, Any]:
        spec = self.open_spec(name)
        B: BaseModel = get_class(spec.schema)
        return B.schema()
        
        
        
    
