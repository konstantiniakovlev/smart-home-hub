import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from src.api.main import app
from src.api.models.devices import DeviceModel
from src.api.backend.session import create_session
from src.api.models.base import Base
from src.api.models.tags import TagModel


class TestMain(unittest.TestCase):
    db_url = "sqlite:///:memory:"

    def setUp(self):
        self.engine = create_engine(
            self.db_url,
            connect_args={"check_same_thread": False}
        )

        Base.metadata.create_all(bind=self.engine)

        TestingSessionLocal = sessionmaker(
            bind=self.engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
        )

        self.session = TestingSessionLocal()

        def override_create_session():
            try:
                yield self.session
            except Exception:
                self.session.rollback()
                raise
            finally:
                self.session.close()


        app.dependency_overrides[create_session] = override_create_session

        # register a test device
        self.test_device = DeviceModel(
            mac_address="18:50:6a:3d:5f:e6",
            ip_address="112.152.169.241",
            device_type="Test Raspberry Pi Pico",
            description="Test device for testing purposes"
        )

        self.test_tag = TagModel(
            name="Dummy tag",
            tag="DUMMY_TAG",
            description="Dummy tag for testing purposes"
        )

        self.session.add(self.test_device)
        self.session.add(self.test_tag)
        self.session.commit()

        self.session.refresh(self.test_device)
        self.session.refresh(self.test_tag)

        self.client = TestClient(app)

    def tearDown(self):
        self.session.close()
        self.engine.dispose()

    def test_get_devices_given_incorrect_device_id_returns_empty_list(self):
        response = self.client.get("/hub/devices?device_id=2")
        response.raise_for_status()
        response_body = response.json()

        self.assertEqual(len(response_body), 0)

    def test_get_devices_given_correct_device_returns_correct_device(self):
        response = self.client.get("/hub/devices?device_id=1")
        response.raise_for_status()
        response_body = response.json()
        device_object = response_body[0]

        self.assertEqual(200, response.status_code)
        self.assertEqual(device_object["device_id"], self.test_device.device_id)
        self.assertEqual(device_object["mac_address"], self.test_device.mac_address)
        self.assertEqual(device_object["ip_address"], self.test_device.ip_address)
        self.assertEqual(device_object["device_type"], self.test_device.device_type)
        self.assertTrue(self.test_device.registered_at)
        self.assertTrue(self.test_device.registered_at)

    def test_get_tags_given_correct_tag_filter_returns_correct_tag(self):
        response = self.client.get("/hub/tags?tag=DUMMY_TAG")
        response.raise_for_status()
        response_body = response.json()
        tag_object = response_body[0]

        self.assertEqual(200, response.status_code)
        self.assertEqual(tag_object["name"], self.test_tag.name)
        self.assertEqual(tag_object["description"], self.test_tag.description)
        self.assertEqual(tag_object["tag"], self.test_tag.tag)

