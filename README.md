## Environment Variables

All environment variables for the bot are stored in `config.json` as follows. Necessary variables are indicated by `<>`, otherwise they are used for testing. If you wantn to directly use the code, fill all the variables.
```json
{
    "bot_prefix": "<BOT_PREFIX>",
    "bot_token": "<BOT_TOKEN>",
    "wk_token": "<WANIKANI_API_TOKEN>",
    "developer_ids": [
        <YOUR_ID>,
    ],
    "application_id": "?APPLICATION_ID?",
    "guild_id": "?GUILD_ID?",
    "channel_ids": {
        "announce": "<ANNOUNCEMENT_CHANNEL_ID>",
        "test": "?TEST_CHANNEL_ID?"
    }
}
```