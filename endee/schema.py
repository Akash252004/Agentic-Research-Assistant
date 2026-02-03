import re
import sys
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from .constants import (
    DEFAULT_EF_SEARCH,
    DEFAULT_TOPK,
    MAX_DIMENSION_ALLOWED,
    MAX_EF_SEARCH_ALLOWED,
    MAX_INDEX_NAME_LENGTH_ALLOWED,
    MAX_TOP_K_ALLOWED,
    PRECISION_TYPES_SUPPORTED,
    SPACE_TYPES_SUPPORTED,
    Precision,
)


class VectorItem(BaseModel):
    """Model for a single vector item in an upsert operation."""

    id: str = Field(..., min_length=1)
    vector: List[float]
    meta: Optional[Dict[str, Any]] = Field(default_factory=dict)
    filter: Optional[Dict[str, Any]] = Field(default_factory=dict)
    sparse_indices: Optional[List[int]] = None
    sparse_values: Optional[List[float]] = None

    @model_validator(mode="after")
    def validate_sparse_data(self) -> "VectorItem":
        if (self.sparse_indices is None) != (self.sparse_values is None):
            raise ValueError(
                "Both sparse_indices and sparse_values must be provided together"
            )
        if self.sparse_indices is not None and len(self.sparse_indices) != len(
            self.sparse_values
        ):
            raise ValueError("sparse_indices and sparse_values must match in length")
        return self


class QueryRequest(BaseModel):
    """Model for query parameters."""

    vector: Optional[List[float]] = None
    top_k: int = Field(default=DEFAULT_TOPK, gt=0, le=MAX_TOP_K_ALLOWED)
    filter: Optional[List[Dict[str, Any]]] = None
    ef: int = Field(default=DEFAULT_EF_SEARCH, le=MAX_EF_SEARCH_ALLOWED)
    include_vectors: bool = False
    sparse_indices: Optional[List[int]] = None
    sparse_values: Optional[List[float]] = None

    @model_validator(mode="after")
    def validate_query_type(self) -> "QueryRequest":
        has_dense = self.vector is not None
        has_sparse = self.sparse_indices is not None or self.sparse_values is not None

        if not has_dense and not has_sparse:
            raise ValueError(
                "At least one of 'vector' or 'sparse_indices'/'sparse_values'"
                " must be provided."
            )

        if (self.sparse_indices is None) != (self.sparse_values is None):
            raise ValueError(
                "Both sparse_indices and sparse_values must be provided together"
            )

        if self.sparse_indices is not None and len(self.sparse_indices) != len(
            self.sparse_values
        ):
            raise ValueError("sparse_indices and sparse_values must match in length")

        return self


class IndexCreateRequest(BaseModel):
    """Model for index creation parameters."""

    name: str
    dimension: int = Field(..., gt=0, le=MAX_DIMENSION_ALLOWED)
    space_type: str
    M: int = Field(..., gt=0)
    ef_con: int = Field(..., gt=0)
    precision: Union[str, Precision]
    version: Optional[int] = None
    sparse_dim: int = Field(default=0, ge=0, le=sys.maxsize)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not re.match(r"^[a-zA-Z0-9_]+$", v):
            raise ValueError(
                "Index name must be alphanumeric and can contain underscores"
            )
        if len(v) > MAX_INDEX_NAME_LENGTH_ALLOWED:
            raise ValueError(
                f"Index name should be less than {MAX_INDEX_NAME_LENGTH_ALLOWED}"
                " characters"
            )
        return v

    @field_validator("space_type")
    @classmethod
    def validate_space_type(cls, v: str) -> str:
        v = v.lower()
        if v not in SPACE_TYPES_SUPPORTED:
            raise ValueError(
                f"Invalid space type: {v}. Must be one of {SPACE_TYPES_SUPPORTED}"
            )
        return v

    @field_validator("precision")
    @classmethod
    def validate_precision(cls, v: Union[str, Precision]) -> Union[str, Precision]:
        if isinstance(v, Precision):
            return v
        if v not in PRECISION_TYPES_SUPPORTED:
            raise ValueError(
                f"Invalid precision: {v}. Must be one of {PRECISION_TYPES_SUPPORTED}"
            )
        return v


class IndexMetadata(BaseModel):
    """Model for index metadata returned by the server."""

    model_config = ConfigDict(populate_by_name=True)

    name: Optional[str] = Field(None, alias="name")
    lib_token: str
    total_elements: int = Field(..., alias="total_elements")
    space_type: str = Field(..., alias="space_type")
    dimension: int = Field(..., alias="dimension")
    precision: Optional[str] = Field(None, alias="precision")
    M: int = Field(..., alias="M")
    sparse_dim: int = Field(0, alias="sparse_dim")
