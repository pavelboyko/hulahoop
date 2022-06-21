import logging


import logging
from typing import Optional, Tuple
from app.models import Example, Issue


logger = logging.getLogger(__package__)


def get_or_create_issue(example: Example) -> Tuple[Optional[Issue], bool]:
    """Find an issue for the example or create a new one (or do nothing and return None, False but this is temporary

    returns: the issue and a boolean value that specifies whether the issue was created or not
    """

    if not example.fingerprint:
        # for now we do not group examples without a fingerprint field
        # to be changed in the future
        return None, False

    issues = Issue.objects.filter(
        project=example.project, fingerprint=example.fingerprint
    )
    if issues:
        the_issue: Issue = issues.first()  # type: ignore
        the_issue.add_example(example)
        the_issue.refresh_from_db()
        return the_issue, False
    else:
        the_issue = Issue.objects.create(
            project=example.project,
            fingerprint=example.fingerprint,
            name=example.fingerprint,  # this is experimental
        )
        the_issue.add_example(example)
        the_issue.refresh_from_db()
        return the_issue, True
