from transpire.resources import ConfigMap, Deployment, Ingress, Service

name = "ocf-io"

NGINX_CONF = """
user nginx;
worker_processes  auto;
pid /var/run/nginx.pid;

events {
    worker_connections  1024;
}

http {
    server {
        listen 80;
        server_name ~^(.+).ocf.io$;

        return 302 $scheme://$1.ocf.berkeley.edu$request_uri;
    }
}
"""


def objects():
    cm = ConfigMap(
        name="ocf-io-nginx",
        data={"nginx.conf": NGINX_CONF},
    )

    dep = Deployment(
        name="ocf-io",
        image="nginx:1.23.4",
        ports=[80],
    )

    dep.obj.spec.template.spec.volumes = [
        {
            "name": "nginx-conf",
            "configMap": {"name": cm.obj.metadata.name},
        },
    ]

    dep.obj.spec.template.spec.containers[0].volume_mounts = [
        {
            "name": "nginx-conf",
            "mountPath": "/etc/nginx/nginx.conf",
            "subPath": "nginx.conf",
        }
    ]

    svc = Service(
        name="ocf-io",
        selector=dep.get_selector(),
        port_on_pod=80,
        port_on_svc=80,
    )

    ing = Ingress.from_svc(
        svc,
        host="*.ocf.io",
        path_prefix="/",
    )

    yield cm.build()
    yield dep.build()
    yield svc.build()
    yield ing.build()
