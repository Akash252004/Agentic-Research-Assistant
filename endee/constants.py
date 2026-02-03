"""
Constants Module for Endee Vector Database Client

This module defines all constants used throughout the Endee client library,
including configuration defaults, supported types and validation limits.
"""

from enum import Enum


class Precision(str, Enum):
    """
    Supported precision types(quanization levels) for vector indices.

    Defines the data types available for storing vector embeddings

    Attributes:
        BINARY2: Binary vectors (1 bit per dimension)
        FLOAT16: 16-bit floating point
        FLOAT32: 32-bit floating point
        INT16D: 16-bit integer
        INT8D: 8-bit integer
    """

    BINARY2 = "binary"
    FLOAT16 = "float16"
    FLOAT32 = "float32"
    INT16D = "int16d"
    INT8D = "int8d"


# Checksum Value while creating an index
CHECKSUM = -1

# HTTP Configuration
# HTTP methods allowed for API requests
HTTP_METHODS_ALLOWED = ["GET", "POST", "PUT", "DELETE", "PATCH"]

# HTTP status codes that trigger automatic retries
HTTP_STATUS_CODES = [429, 500, 502, 503, 504]

# Protocol prefixes for URL mounting
HTTPS_PROTOCOL = "https://"
HTTP_PROTOCOL = "http://"


# API Endpoints
LOCAL_BASE_URL = "http://127.0.0.1:8080/api/v1"


# Vector Index Limits
# Maximum vector dimensionality allowed
MAX_DIMENSION_ALLOWED = 10000

# Maximum number of vectors that can be inserted in a single batch operation
MAX_VECTORS_PER_BATCH = 1000

# Maximum number of nearest neighbors (top-k) that can be retrieved
MAX_TOP_K_ALLOWED = 512

# Maximum ef_search parameter for HNSW query accuracy
MAX_EF_SEARCH_ALLOWED = 1024

# Maximum length for index names (alphanumeric + underscores)
MAX_INDEX_NAME_LENGTH_ALLOWED = 48


# Default region for local deployments
LOCAL_REGION = "local"


# Supported Types
# List of precision types supported by the vector database
PRECISION_TYPES_SUPPORTED = ["binary", "float16", "float32", "int16d", "int8d"]

# Distance metric types
COSINE = "cosine"  # Cosine similarity (normalized dot product)
L2 = "l2"  # Euclidean distance (L2 norm)
INNER_PRODUCT = "ip"  # Inner product (dot product)

# List of supported distance/space types
SPACE_TYPES_SUPPORTED = [COSINE, L2, INNER_PRODUCT]


# HTTP Library Options
# Use requests library for HTTP operations
HTTP_REQUESTS_LIBRARY = "requests"

# Use httpx library with HTTP/1.1 protocol
HTTP_HTTPX_1_1_LIBRARY = "httpx1.1"

# Use httpx library with HTTP/2 protocol
HTTP_HTTPX_2_LIBRARY = "httpx2"


# API Field Names
# Common field names used in API requests/responses
AUTHORIZATION_HEADER = "Authorization"
NAME_FIELD = "name"
SPACE_TYPE_FIELD = "space_type"
DIMENSION_FIELD = "dimension"
SPARSE_DIM_FIELD = "sparse_dim"
IS_HYBRID_FIELD = "is_hybrid"
COUNT_FIELD = "count"
PRECISION_FIELD = "precision"
MAX_CONNECTIONS_FIELD = "M"


# Requests Library Session Configuration
# Number of connection pools to cache (one per unique host)
SESSION_POOL_CONNECTIONS = 1

# Maximum number of connections to save in each pool for reuse
# Higher values allow more concurrent requests to the same host
SESSION_POOL_MAXSIZE = 10

# Maximum number of retry attempts for failed requests
SESSION_MAX_RETRIES = 3


# HTTPX Library Client Configuration
# Same configuration for both httpx1.1 and httpx2
# Maximum total connections across all hosts
HTTPX_MAX_CONNECTIONS = 1

# Maximum idle connections to keep alive for reuse
# Keepalive connections improve performance by avoiding connection overhead
HTTPX_MAX_KEEPALIVE_CONNECTIONS = 10

# Maximum number of retry attempts for failed requests
HTTPX_MAX_RETRIES = 3

# Request timeout in seconds (prevents hanging requests)
HTTPX_TIMEOUT_SEC = 30.0


# HNSW Algorithm Defaults
# Default M parameter: number of bi-directional links per node in HNSW graph
# Higher values improve recall but increase memory usage and build time
DEFAULT_M = 16

# Default ef_construction: size of dynamic candidate list during index construction
# Higher values improve index quality but slow down construction
DEFAULT_EF_CON = 128

# Default sparse dimension (0 means dense-only vectors, no sparse component)
DEFAULT_SPARSE_DIMENSION = 0

# Default number of nearest neighbors to return in search queries
DEFAULT_TOPK = 10

# Default ef_search: size of dynamic candidate list during search
# Higher values improve recall but slow down queries
DEFAULT_EF_SEARCH = 128
