import os
import unittest
from unittest.mock import patch

import qrcode as qrc

from wechatter.commands._commands import qrcode


class TestQrCodeCommand(unittest.TestCase):
    def setUp(self):
        self.img = qrc.QRCode().make_image()
        self.path = "tests/commands/test_qrcode/test_qrcode.png"

    def tearDown(self):
        if os.path.exists(self.path):
            os.remove(self.path)

    def test_generate_qrcode_success(self):
        result = qrcode._generate_qrcode("https://www.baidu.com")
        self.assertIsInstance(result, qrc.image.pil.PilImage)

    def test_save_qrcode_attribute_error(self):
        with self.assertRaises(AttributeError):
            qrcode._save_qrcode(None, self.path)

    def test_save_qrcode_successfully(self):
        qrcode._save_qrcode(self.img, self.path)
        self.assertTrue(os.path.exists(self.path))

    @patch("os.access", return_value=False)
    def test_save_qrcode_permission_error(self, mock_access):
        with self.assertRaises(PermissionError):
            qrcode._save_qrcode(self.img, self.path)
