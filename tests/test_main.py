import os
import datetime
import unittest

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from src.api.main import app
from src.api.backend.session import create_session, create_async_session
from src.api.models.base import Base
from src.api.models.devices import DeviceModel
from src.api.models.measurements import MeasurementModel
from src.api.models.tags import TagModel


class TestMain(unittest.TestCase):
    # using file-based SQLite to use one db. In memory creates two.
    db_url = "sqlite:///./test.db"
    db_async_url = "sqlite+aiosqlite:///./test.db"

    def setUp(self):
        self.engine = create_engine(self.db_url)
        self.async_engine = create_async_engine(self.db_async_url)

        Base.metadata.create_all(bind=self.engine)

        TestingSessionLocal = sessionmaker(
            bind=self.engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
        )

        AsyncTestingSessionLocal = async_sessionmaker(
            bind=self.async_engine,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False,
        )

        self.session = TestingSessionLocal()
        self.async_session = AsyncTestingSessionLocal()


        def override_create_session():
            try:
                yield self.session
            except Exception:
                self.session.rollback()
                raise
            finally:
                self.session.close()

        async def override_create_async_session():
            async with self.async_session as session:
                try:
                    yield session
                    await session.commit()
                except Exception:
                    await session.rollback()
                    raise
                finally:
                    await session.close()


        app.dependency_overrides[create_session] = override_create_session
        app.dependency_overrides[create_async_session] = override_create_async_session

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

        self.test_measurement = MeasurementModel(
            time=datetime.datetime(2025, 1, 1, 12, 0, 0),
            device_id=1,
            sensor_tag="DUMMY_TAG",
            value=123.456
        )

        self.session.add(self.test_device)
        self.session.add(self.test_tag)
        self.session.add(self.test_measurement)

        self.session.commit()

        self.session.refresh(self.test_device)
        self.session.refresh(self.test_tag)
        self.session.refresh(self.test_measurement)

        self.client = TestClient(app)

    def tearDown(self):
        self.session.close()
        self.engine.dispose()

        self.async_session.close()
        self.async_engine.dispose()

        if os.path.exists("test.db"):
            os.remove("test.db")

    def test_get_devices_given_incorrect_device_id_returns_empty_list(self):
        response = self.client.get("/hub/devices?device_id=2")
        response_body = response.json()

        self.assertEqual(len(response_body), 0)

    def test_get_devices_given_correct_device_returns_correct_device(self):
        response = self.client.get("/hub/devices?device_id=1")
        response_body = response.json()
        device_object = response_body[0]

        self.assertEqual(200, response.status_code)
        self.assertEqual(device_object["device_id"], self.test_device.device_id)
        self.assertEqual(device_object["mac_address"], self.test_device.mac_address)
        self.assertEqual(device_object["ip_address"], self.test_device.ip_address)
        self.assertEqual(device_object["device_type"], self.test_device.device_type)
        self.assertTrue(self.test_device.registered_at)
        self.assertTrue(self.test_device.updated_at)

    def test_get_tags_given_correct_tag_filter_returns_correct_tag(self):
        response = self.client.get("/hub/tags?tag=DUMMY_TAG")
        response_body = response.json()
        tag_object = response_body[0]

        self.assertEqual(200, response.status_code)
        self.assertEqual(tag_object["name"], self.test_tag.name)
        self.assertEqual(tag_object["description"], self.test_tag.description)
        self.assertEqual(tag_object["tag"], self.test_tag.tag)


    def test_get_measurements_given_correct_id_returns_correct_measurement(self):
        response = self.client.get("/hub/measurements/1")
        response_body = response.json()
        measurement_object = response_body[0]

        self.assertEqual(200, response.status_code)
        self.assertEqual(measurement_object["time"], self.test_measurement.time.strftime("%Y-%m-%dT%H:%M:%S"))
        self.assertEqual(measurement_object["device_id"], self.test_measurement.device_id)
        self.assertEqual(measurement_object["sensor_tag"], self.test_measurement.sensor_tag)
        self.assertEqual(measurement_object["value"], self.test_measurement.value)


    def test_get_measurements_given_incorrect_device_id_returns_400(self):
        response = self.client.get("/hub/measurements/2")

        self.assertEqual(400, response.status_code)
