from __future__ import annotations

import importlib
import logging
import os
import sys
from abc import ABCMeta, abstractmethod
from os import path
from typing import TYPE_CHECKING, Any, Dict, Optional, Union

from datayoga_core import Context, utils
from jsonschema import validate

if TYPE_CHECKING:
    from datayoga_core.block import Block
    from datayoga_core.producer import Producer

logger = logging.getLogger("dy")


class Entity(metaclass=ABCMeta):
    INTERNAL_FIELD_PREFIX = "__$$"
    MSG_ID_FIELD = f"{INTERNAL_FIELD_PREFIX}msg_id"
    RESULT_FIELD = f"{INTERNAL_FIELD_PREFIX}result"
    OPCODE_FIELD = f"{INTERNAL_FIELD_PREFIX}opcode"
    """
    Block

    Attributes:
        properties Dict[str, Any]: Block properties
    """

    def __init__(self, properties: Optional[Dict[str, Any]] = None):
        """
        Constructs a block

        Args:
            properties (Optional[Dict[str, Any]]): Block [properties]
        """
        self.properties = properties or {}
        self.validate()

    @abstractmethod
    def init(self, context: Optional[Context] = None):
        """
        Initializes block

        Args:
            context (Context, optional): Context. Defaults to None.
        """
        raise NotImplementedError

    def validate(self):
        """
        Validates block against its JSON Schema
        """
        logger.debug(f"validating {self.properties}")
        validate(instance=self.properties, schema=self.get_json_schema())

    def get_json_schema(self) -> Dict[str, Any]:
        """
        Returns the JSON Schema for this block

        Returns:
            Dict[str, Any]: JSON Schema
        """
        json_schema_file = path.join(
            utils.get_bundled_dir(),
            os.path.relpath(
                os.path.dirname(sys.modules[self.__module__].__file__),
                start=os.path.dirname(__file__)),
            "block.schema.json") if utils.is_bundled() else path.join(
            os.path.dirname(os.path.realpath(sys.modules[self.__module__].__file__)),
            "block.schema.json")
        logger.debug(f"loading schema from {json_schema_file}")
        return utils.read_json(json_schema_file)

    def get_block_name(self):
        return os.path.basename(os.path.dirname(sys.modules[self.__module__].__file__))

    @staticmethod
    def create(block_name: str, properties: Dict[str, Any]) -> Union['Block', 'Producer']:
        module_name = f"datayoga_core.blocks.{block_name}.block"
        module = importlib.import_module(module_name)
        return getattr(module, "Block")(properties)
