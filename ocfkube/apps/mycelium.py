from ocfkube.utils import helm
from ocfkube.utils import versions

values = {}


def build() -> object:
    return helm.build_chart_from_versions(
        name="mycelium",
        versions=versions,
        values=values,
    )
