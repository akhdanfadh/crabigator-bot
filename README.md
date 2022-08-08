## config.json

My current configuration file (subject to change). Change necessary part for your server:
```json
{
    "bot_version": "0.1.0",
    "bot_prefix": "wk!",
    "bot_token": "<YOUR_BOT_TOKEN>",
    "wk_token": "<YOUR_WANIKANI_API_TOKEN (not yet necessary)>",
    "developer_ids": [
        <YOUR_ID>,
    ],
    "application_id": "<YOUR_APPLICATION_ID (not necessary)>",
    "guild_id": "<YOUR_GUILD_ID (not necessary)>",
    "channel_ids": {
        "announce": "<YOUR_CHANNEL_ID (for announcement)>",
        "test": "<YOUR_CHANNEL_ID (for testing, not necessary)>"
    }
}
```