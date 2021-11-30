from ocfkube.lib.ingress import Ingress
from ocfkube.utils import helm
from ocfkube.utils import versions

values = {}

license = [
    {
        "apiVersion": "v1",
        "kind": "Secret",
        "metadata": {
            "labels": {"license.k8s.elastic.co/scope": "operator"},
            "name": "eck-license",
        },
        "type": "Opaque",
        "stringData": {"license": "this is a dummy value, *not* a real license"},
    },
    {
        "apiVersion": "elasticsearch.k8s.elastic.co/v1",
        "kind": "Elasticsearch",
        "metadata": {"name": "elastic"},
        "spec": {
            "version": "7.15.1",
            "nodeSets": [
                {
                    "name": "default",
                    "count": 1,
                    # TODO: This is bad! https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-virtual-memory.html
                    "config": {"node.store.allow_mmap": False},
                    # workaround for https://github.com/elastic/cloud-on-k8s/issues/4334
                    "podTemplate": {
                        "spec": {
                            "containers": [
                                {
                                    "name": "elasticsearch",
                                    "securityContext": {
                                        "capabilities": {"add": ["SYS_CHROOT"]}
                                    },
                                }
                            ]
                        }
                    },
                }
            ],
        },
    },
    {
        "apiVersion": "kibana.k8s.elastic.co/v1",
        "kind": "Kibana",
        "metadata": {"name": "elastic"},
        "spec": {
            "version": "7.15.1",
            "count": 1,
            "elasticsearchRef": {"name": "elastic"},
            "enterpriseSearchRef": {"name": "ocf"},
        },
    },
    {
        "apiVersion": "enterprisesearch.k8s.elastic.co/v1",
        "kind": "EnterpriseSearch",
        "metadata": {"name": "ocf"},
        "spec": {
            "version": "7.15.1",
            "count": 1,
            "elasticsearchRef": {"name": "elastic"},
        },
    },
]


def build() -> object:
    ingress = Ingress.from_service_name(
        "elastic-kb-http", "5601", "kibana.ocf.berkeley.edu"
    ).data

    return (
        helm.build_chart_from_versions(name="elastic", versions=versions, values=values)
        + license
        + [ingress]
    )
