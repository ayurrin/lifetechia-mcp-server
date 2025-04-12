## EDINET DATA MCP Server From Lifetechia

Get API key From [here](https://lifetechia.com/register/) It is Free!

for MCP server settings
```json
{
    "lifetechia": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e",
        "API_KEY",
        "lifetechia-server"
      ],
      "env": {
        "API_KEY": "APIKEY"
      },
      "autoApprove": [],
      "disabled": false,
      "timeout": 60,
      "transportType": "stdio"
    },
}
```