from dataclasses import asdict, is_dataclass, make_dataclass
import json
import yaml
import toml


def serialize(cls):
    if not is_dataclass(cls):
        make_dataclass(cls.__name__, cls.__annotations__)

    def to_json(self, **kwargs):
        return json.dumps(asdict(self), **kwargs)

    @classmethod
    def from_json(cls, json_str):
        return cls(**json.loads(json_str))

    cls.to_json = to_json
    cls.from_json = from_json

    def to_yaml(self, **kwargs):
        return yaml.dump(asdict(self), **kwargs)

    @classmethod
    def from_yaml(cls, yaml_str):
        return cls(**yaml.safe_load(yaml_str))

    cls.to_yaml = to_yaml
    cls.from_yaml = from_yaml

    def to_toml(self, **kwargs):
        return toml.dumps(asdict(self), **kwargs)

    @classmethod
    def from_toml(cls, toml_str):
        return cls(**toml.loads(toml_str))

    cls.to_toml = to_toml
    cls.from_toml = from_toml

    return cls
