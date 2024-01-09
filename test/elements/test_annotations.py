import unittest

from grafana_client import GrafanaApi
from grafana_client.client import (
    GrafanaBadInputError,
    GrafanaClientError,
    GrafanaServerError,
    GrafanaUnauthorizedError,
)

from ..compat import requests_mock


class AnnotationsTestCase(unittest.TestCase):
    def setUp(self):
        self.grafana = GrafanaApi(("admin", "admin"), host="localhost", url_path_prefix="", protocol="http")

    @requests_mock.Mocker()
    def test_annotations(self, m):
        m.get(
            "http://localhost/api/annotations?from=1563183710618&to=1563185212275"
            "&alertId=11&dashboardId=111&dashboardUID=v1Mm5FPVz&panelId=22&userId=42&type=alert&tags=tags-test&limit=1",
            json=[
                {
                    "id": 80,
                    "alertId": 11,
                    "alertName": "",
                    "dashboardId": 111,
                    "dashboardUID": "v1Mm5FPVz",
                    "panelId": 22,
                    "userId": 42,
                    "type": "alert",
                    "newState": "",
                    "prevState": "",
                    "created": 1563280160455,
                    "updated": 1563280160455,
                    "time": 1563156456006,
                    "text": "Annotation Description",
                    "tags": ["tags-test"],
                    "login": "",
                    "email": "",
                    "avatarUrl": "",
                    "data": {},
                },
            ],
            headers={"Content-Type": "application/json"},
        )
        annotations = self.grafana.annotations.get_annotation(
            time_from=1563183710618,
            time_to=1563185212275,
            alert_id=11,
            dashboard_id=111,
            dashboard_uid="v1Mm5FPVz",
            panel_id=22,
            user_id=42,
            ann_type="alert",
            tags=["tags-test"],
            limit=1,
        )
        self.assertEqual(annotations[0]["text"], "Annotation Description")
        self.assertEqual(annotations[0]["alertId"], 11)
        self.assertEqual(annotations[0]["dashboardUID"], "v1Mm5FPVz")
        self.assertEqual(annotations[0]["dashboardId"], 111)
        self.assertEqual(annotations[0]["panelId"], 22)
        self.assertEqual(annotations[0]["userId"], 42)
        self.assertEqual(annotations[0]["type"], "alert")
        self.assertEqual(annotations[0]["tags"][0], "tags-test")

        self.assertEqual(len(annotations), 1)

    @requests_mock.Mocker()
    def test_annotations_with_out_param(self, m):
        m.get(
            "http://localhost/api/annotations",
            json=[
                {
                    "id": 80,
                    "alertId": 11,
                    "alertName": "",
                    "dashboardId": 111,
                    "panelId": 22,
                    "userId": 0,
                    "newState": "",
                    "prevState": "",
                    "created": 1563280160455,
                    "updated": 1563280160455,
                    "time": 1563156456006,
                    "text": "Annotation Description",
                    "tags": ["tags-test"],
                    "login": "",
                    "email": "",
                    "avatarUrl": "",
                    "data": {},
                },
            ],
            headers={"Content-Type": "application/json"},
        )
        annotations = self.grafana.annotations.get_annotation()
        self.assertEqual(len(annotations), 1)

    @requests_mock.Mocker()
    def test_delete_annotations_by_id(self, m):
        m.delete(
            "http://localhost/api/annotations/99",
            json={"message": "Annotation deleted"},
            headers={"Content-Type": "application/json"},
        )
        annotation = self.grafana.annotations.delete_annotations_by_id(annotations_id=99)
        self.assertEqual(annotation["message"], "Annotation deleted")

    @requests_mock.Mocker()
    def test_delete_annotations_by_id_could_not_find(self, m):
        m.delete(
            "http://localhost/api/annotations/None",
            json={"message": "Could not find annotation to update"},
            status_code=500,
            headers={"Content-Type": "application/json"},
        )
        with self.assertRaises(GrafanaServerError):
            self.grafana.annotations.delete_annotations_by_id(annotations_id=None)

    @requests_mock.Mocker()
    def test_delete_annotations_by_id_forbidden(self, m):
        m.delete(
            "http://localhost/api/annotations/None",
            json={"message": "Forbidden"},
            status_code=403,
            headers={"Content-Type": "application/json"},
        )
        with self.assertRaises(GrafanaClientError):
            self.grafana.annotations.delete_annotations_by_id(annotations_id=None)

    @requests_mock.Mocker()
    def test_delete_annotations_by_id_unauthorized(self, m):
        m.delete(
            "http://localhost/api/annotations/None",
            json={"message": "Unauthorized"},
            status_code=401,
            headers={"Content-Type": "application/json"},
        )
        with self.assertRaises(GrafanaUnauthorizedError):
            self.grafana.annotations.delete_annotations_by_id(annotations_id=None)

    @requests_mock.Mocker()
    def test_delete_annotations_by_id_bad_input(self, m):
        m.delete(
            "http://localhost/api/annotations/None",
            json={"message": "Bad Input"},
            status_code=400,
            headers={"Content-Type": "application/json"},
        )
        with self.assertRaises(GrafanaBadInputError):
            self.grafana.annotations.delete_annotations_by_id(annotations_id=None)

    @requests_mock.Mocker()
    def test_add_annotation_no_dashboard(self, m):
        m.post(
            "http://localhost/api/annotations",
            json={"endId": 80, "id": 79, "message": "Annotation added"},
            headers={"Content-Type": "application/json"},
        )
        annotation = self.grafana.annotations.add_annotation(
            time_from=1563183710618, time_to=1563185212275, tags=["tags-test"], text="Test"
        )
        self.assertEqual(annotation["endId"], 80)
        self.assertEqual(annotation["id"], 79)
        self.assertEqual(annotation["message"], "Annotation added")

    @requests_mock.Mocker()
    def test_add_annotation_dashboard_id(self, m):
        m.post(
            "http://localhost/api/annotations",
            json={"dashboardId": 42},
            headers={"Content-Type": "application/json"},
        )
        annotation = self.grafana.annotations.add_annotation(
            dashboard_id=42, time_from=1563183710618, time_to=1563185212275, tags=["tags-test"], text="Test"
        )
        self.assertEqual(annotation["dashboardId"], 42)

    @requests_mock.Mocker()
    def test_add_annotation_dashboard_uid(self, m):
        m.post(
            "http://localhost/api/annotations",
            json={"dashboardUID": "jcIIG-07z"},
            headers={"Content-Type": "application/json"},
        )
        annotation = self.grafana.annotations.add_annotation(
            dashboard_uid="jcIIG-07z", time_from=1563183710618, time_to=1563185212275, tags=["tags-test"], text="Test"
        )
        self.assertEqual(annotation["dashboardUID"], "jcIIG-07z")

    @requests_mock.Mocker()
    def test_update_annotation(self, m):
        m.put(
            "http://localhost/api/annotations/79",
            json={"endId": 80, "id": 79, "message": "Annotation updated"},
            headers={"Content-Type": "application/json"},
        )
        annotation = self.grafana.annotations.update_annotation(
            annotations_id=79, time_from=1563183710618, time_to=1563185212275, tags=["tags-test"], text="Test"
        )
        self.assertEqual(annotation["endId"], 80)
        self.assertEqual(annotation["id"], 79)
        self.assertEqual(annotation["message"], "Annotation updated")

    @requests_mock.Mocker()
    def test_partial_update_annotation(self, m):
        m.patch(
            "http://localhost/api/annotations/89",
            json={"message": "Annotation patched"},
            headers={"Content-Type": "application/json"},
        )
        annotation = self.grafana.annotations.partial_update_annotation(
            annotations_id=89, tags=["tag1", "tag2"], text="Test"
        )
        self.assertEqual(annotation["message"], "Annotation patched")

    @requests_mock.Mocker()
    def test_add_annotation_graphite(self, m):
        m.post(
            "http://localhost/api/annotations/graphite",
            json={"message": "Graphite annotation added", "id": 1},
            headers={"Content-Type": "application/json"},
        )
        annotation = self.grafana.annotations.add_annotation_graphite(
            what="Event - deploy", tags=["deploy", "production"], when=1467844481, data="Data"
        )

        self.assertEqual(annotation["id"], 1)
        self.assertEqual(annotation["message"], "Graphite annotation added")
