class DuplicateCategoryException(Exception):
    """Exception indicating a Category of the same name exists."""


class DuplicateTallyException(Exception):
    """Exception for creating a tally that exists under the same category."""
