import unittest
from datetime import datetime

import model
from database import Session, init_database
from database.save import save_discord_message
from tests.utils.implementations import (
    MockDiscordAsset,
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

    def testSimpleMessage(self):
        message = MockDiscordMessage(
            id=1234,
            created_at=datetime(2023, 1, 1, 9, 0, 0),
            content="hello world",
            author=self.user1,
            channel=self.channel1,
        )

        save_discord_message(message)

        with Session() as session:
            result_message: model.Message = session.query(model.Message).get(message.id)
            self.assertIsNotNone(result_message)
            self.assertEqual(result_message.created_at, message.created_at)
            self.assertEqual(result_message.content, message.content)
            self.assertEqual(result_message.author_id, message.author.id)
            self.assertEqual(result_message.channel_id, message.channel.id)
            self.assertEqual(result_message.jump_url, message.jump_url)

            result_channel: model.Channel = session.query(model.Channel).get(
                message.channel.id
            )
            self.assertIsNotNone(result_channel)
            self.assertEqual(result_channel.name, message.channel.name)
            self.assertFalse(result_channel.thread)

            result_author: model.User = session.query(model.User).get(message.author.id)
            self.assertIsNotNone(result_author)
            self.assertEqual(result_author.username, message.author.username)
            self.assertEqual(
                result_author.avatar_url, message.author.display_avatar.url
            )


if __name__ == "__main__":
    unittest.main()
