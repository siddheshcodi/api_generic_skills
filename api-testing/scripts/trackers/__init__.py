"""Bug tracker adapters. To add one: create <name>.py with a Tracker subclass and register it here."""
from .jira import Jira
from .manual import Manual
from .proofhub import ProofHub
from .trello import Trello

ADAPTERS = {"proofhub": ProofHub, "jira": Jira, "trello": Trello, "manual": Manual}
