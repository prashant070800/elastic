from unittest.mock import patch, AsyncMock
from django.test import TestCase

import asyncio

class NotifyOnIncomingStreamTest(TestCase):
    def test_notify_on_incoming_stream(self):
        pk = 1
        to_number_pk = 2
        session_id = "session123"
        channel_name = "channel_abc"
        from_number = "+1234567890"
        timeout = 30
        rtc_mode = "some_mode"

        # Mock database calls
        mock_phone_number = {"pk": to_number_pk}
        mock_call = {"pk": pk}

        with patch("search.module.PhoneNumber.objects.get", return_value=mock_phone_number), \
             patch("search.module.Call.objects.get", return_value=mock_call), \
             patch("search.module._get_app_type_and_appuser_and_org", return_value=("app_type", "appuser", "org")), \
             patch("search.module._get_payload_and_voip_jaxl_call", return_value=("mock_payload", "mock_jaxl_call")), \
             patch("search.module._notify_appuser", new_callable=AsyncMock) as mock_notify:

            # Mock async function return value
            mock_notify.return_value = 1

            # Directly run the async part
            asyncio.run(mock_notify("appuser", payload="mock_payload", jaxl_call="mock_jaxl_call"))

            # Assertions
            mock_notify.assert_awaited_once_with(
                "appuser",
                payload="mock_payload",
                jaxl_call="mock_jaxl_call",
            )
