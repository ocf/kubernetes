from ocfkube.utils import helm
from ocfkube.utils import versions

values = {
    "global": {
        "hosts": {
            "domain": "ocf.berkeley.edu" # GitLab automatically prepends "gitlab."
            "https": False
        },
        "grafana": {
            "enabled": True
        },
        "edition": "ce"
    },
    "ldap": {
        "preventSignin": False,
        "servers": {
            "ocf": {
                "label": "LDAP",
                "host": "firestorm.ocf.berkeley.edu",
                "port": 636,
                "uid": "uid",
                "base": "dc=OCF,dc=Berkeley,dc=EDU",
                "password": {
                    "secret": "my-ldap-password-secret",
                    "key": "the-key-containing-the-password"
                }
            }
        }
    }
}


def build() -> object:
    return helm.build_chart_from_versions(
        name="gitlab",
        versions=versions,
        values=values,
    )
