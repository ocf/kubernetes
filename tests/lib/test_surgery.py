import pytest

from ocfkube.lib.surgery import edit_manifests, make_edit_manifest


class TestEditManifest:
    def make_manifest(self, apiVersion, kind, name):
        return {
            "apiVersion": apiVersion,
            "kind": kind,
            "metadata": {"name": name},
        }

    def test_basic(self):
        const = lambda v: lambda x: v  # noqa: E731

        manifests = [
            self.make_manifest("v1", "Service", "svc1"),
            self.make_manifest("v1", "Service", "svc2"),
            self.make_manifest("networking.k8s.io/v1", "Ingress", "ingress1"),
            self.make_manifest("networking.k8s.io/v1", "Ingress", "ingress2"),
        ]
        edited = edit_manifests(
            {
                ("Service", "svc1"): const("svc1"),
                ("Ingress", "ingress1"): const("ingress1"),
            },
            manifests,
        )
        assert edited == [
            "svc1",
            self.make_manifest("v1", "Service", "svc2"),
            "ingress1",
            self.make_manifest("networking.k8s.io/v1", "Ingress", "ingress2"),
        ]

    def test_unapplied_edit(self):
        id = lambda x: x  # noqa: E731

        manifests = [
            self.make_manifest("v1", "Service", "name1"),
            self.make_manifest("v1", "Secret", "name2"),
            self.make_manifest("extensions/v1beta1", "Ingress", "name3"),
        ]
        with pytest.raises(
            RuntimeError, match=r"Some edits were not applied:.*Service.*name2"
        ):
            edit_manifests({("Service", "name2"): id}, manifests)
        with pytest.raises(
            RuntimeError, match=r"Some edits were not applied:.*Ingress.*name1"
        ):
            edit_manifests({("Ingress", "name1"): id}, manifests)
        with pytest.raises(
            RuntimeError,
            match=r"Some edits were not applied:.*networking\.k8s\.io/v1.*Ingress.*name3",
        ):
            edit_manifests(
                {(("networking.k8s.io/v1", "Ingress"), "name3"): id}, manifests
            )


class TestMakeEditManifest:
    def test_basic(self):
        obj = {"a": {"b": {"c": "foo"}, "d": 1}}
        expected = {"a": {"b": {"c": "bar"}, "d": 2, "new": "value"}}
        edit = make_edit_manifest(
            {
                ("a", "b", "c"): "bar",
                ("a", "d"): 2,
                ("a", "new"): "value",
            }
        )
        assert edit(obj) == expected
        assert obj == expected

    def test_with_edit_manifests(self):
        manifests = [
            {
                "apiVersion": "v1",
                "kind": "Service",
                "metadata": {
                    "name": "svc-1",
                    "annotations": {"ocf.io/test": "yes"},
                },
                "spec": {"dummy": "foo"},
            },
            {
                "apiVersion": "v1",
                "kind": "Service",
                "metadata": {
                    "name": "svc-2",
                    "annotations": {"ocf.io/test": "yes"},
                },
                "spec": {"dummy": "foo"},
            },
        ]
        expected = [
            {
                "apiVersion": "v1",
                "kind": "Service",
                "metadata": {
                    "name": "svc-1",
                    "annotations": {"ocf.io/test": "no"},
                },
                "spec": {"dummy": "bar"},
            },
            {
                "apiVersion": "v1",
                "kind": "Service",
                "metadata": {
                    "name": "svc-2",
                    "annotations": {"ocf.io/test": "yes"},
                },
                "spec": {"dummy": "foo"},
            },
        ]
        assert (
            edit_manifests(
                {
                    ("Service", "svc-1"): make_edit_manifest(
                        {
                            ("metadata", "annotations", "ocf.io/test"): "no",
                            ("spec", "dummy"): "bar",
                        }
                    ),
                },
                manifests,
            )
            == expected
        )
