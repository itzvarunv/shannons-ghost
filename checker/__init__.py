"""The non-AI checker: parse topics, compare their form, verify proposed mappings."""
from .mapping import check_mapping
from .parse import Parsed, TopicError, parse_topic
from .signature import form_check, signature

__all__ = ["Parsed", "TopicError", "parse_topic", "signature", "form_check", "check_mapping"]
