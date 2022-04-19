from transpire.dsl import helm
from apps.versions import versions

from transpire.dsl import emit


def build() -> None:
    emit(
        helm.build_chart_from_versions(
            name="mycelium",
            versions=versions,
            values={},
        )
    )
