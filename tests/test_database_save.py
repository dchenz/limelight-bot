import unittest
from datetime import datetime

from database import Session, init_database, model
from database.queries import save_discord_message
from tests.utils.implementations import (
    MockDiscordAsset,
    MockDiscordAttachment,
    MockDiscordChannel,
    MockDiscordMessage,
    MockDiscordUser,
)


class TestSaveDiscordMessage(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user1 = MockDiscordUser(
            id=2345,
            name="hello",
            discriminator="0000",
            display_avatar=MockDiscordAsset(url="fake url"),
        )
        self.channel1 = MockDiscordChannel(id=3456, name="general")

    def setUp(self):
        init_database("sqlite:///:memory:", debug=True)

    def tearDown(self):
        Session.remove()

    def assertMessagesEqual(
        self, model_obj: model.Message, mock_obj: MockDiscordMessage
    ):
        self.assertEqual(model_obj.uid, mock_obj.id)
        self.assertEqual(model_obj.created_at, mock_obj.created_at)
        self.assertEqual(model_obj.content, mock_obj.content)
        self.assertEqual(model_obj.author_id, mock_obj.author.id)
        self.assertEqual(model_obj.channel_id, mock_obj.channel.id)
        self.assertEqual(model_obj.jump_url, mock_obj.jump_url)

        self.assertEqual(model_obj.channel_id, mock_obj.channel.id)
        self.assertEqual(model_obj.channel.name, mock_obj.channel.name)

        self.assertEqual(model_obj.author.username, mock_obj.author.username)
        self.assertEqual(
            model_obj.author.avatar_url, mock_obj.author.display_avatar.url
        )

    def assertAttachmentsEqual(
        self, model_obj: model.Attachment, mock_obj: MockDiscordAttachment
    ):
        self.assertEqual(model_obj.uid, mock_obj.id)
        self.assertEqual(model_obj.filename, mock_obj.filename)
        self.assertEqual(model_obj.content_type, mock_obj.content_type)
        self.assertEqual(model_obj.size, mock_obj.size)
        self.assertEqual(model_obj.url, mock_obj.url)
        self.assertEqual(model_obj.proxy_url, mock_obj.proxy_url)
        self.assertEqual(model_obj.width, mock_obj.width)
        self.assertEqual(model_obj.height, mock_obj.height)

    def testSimpleMessage(self):
        message = MockDiscordMessage(
            id=1234,
            created_at=datetime(2023, 1, 1, 9, 0, 0),
            content="hello world 1",
            author=self.user1,
            channel=self.channel1,
        )

        save_discord_message(message)

        with Session() as session:
            result: model.Message = session.query(model.Message).get(message.id)
            self.assertIsNotNone(result)
            self.assertMessagesEqual(result, message)

    def testMessageWithAttachments(self):
        attachment1 = MockDiscordAttachment(
            id=1000,
            filename="screenshot.png",
            content_type="image/png",
            size=50000,
            url="url 1",
            proxy_url="proxy url 1",
            width=600,
            height=400,
        )
        attachment2 = MockDiscordAttachment(
            id=1001,
            filename="resume.pdf",
            content_type="application/pdf",
            size=12345,
            url="url 2",
            proxy_url="proxy url 2",
            width=None,
            height=None,
        )
        message = MockDiscordMessage(
            id=1234,
            created_at=datetime(2023, 1, 1, 9, 0, 0),
            content="hello world 2",
            author=self.user1,
            channel=self.channel1,
            attachments=[attachment1, attachment2],
        )

        save_discord_message(message)

        with Session() as session:
            result: model.Message = session.query(model.Message).get(message.id)
            self.assertIsNotNone(result)
            self.assertMessagesEqual(result, message)
            self.assertEqual(len(result.attachments), 2)
            self.assertAttachmentsEqual(result.attachments[0], attachment1)
            self.assertAttachmentsEqual(result.attachments[1], attachment2)


if __name__ == "__main__":
    unittest.main()
