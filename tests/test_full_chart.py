"""Test the complete chart for sweeping requirements"""

from tests.helm_template_generator import render_chart
import jmespath
import pytest
from . import supported_k8s_versions
import pytest_check as check


@pytest.mark.parametrize(
    "kube_version",
    supported_k8s_versions,
)
class TestIngress:
    def test_container_probes(self, kube_version):
        """Ensure all containers have liveness and readiness probes

        - https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#when-should-you-use-a-liveness-probe
        - https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#when-should-you-use-a-readiness-probe
        """
        docs = render_chart(
            kube_version=kube_version,
        )
        # TODO: Find a way to parametrize these tests so they show up as individual tests, not just TestIngress.test_container_probes[1.16.0]
        # TODO: Find a way to exclude some containers from probes (EG: cronjobs)
        # TODO: Find a way to show which template the missing probe came from? Not sure if this is super valuable, just trying to give the user more hints as to where to make a fix
        specs = jmespath.search(
            "[*].spec.template.spec.containers[*].{name: name, livenessProbe: contains(keys(@),'livenessProbe'), readinessProbe: contains(keys(@),'readinessProbe')}",
            docs,
        )

        for containers in specs:
            for container in containers:
                check.is_true(
                    all([container["readinessProbe"], container["livenessProbe"]]),
                    f"Needs probes: {container}",
                )
