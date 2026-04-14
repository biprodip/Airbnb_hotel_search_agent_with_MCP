"""MCP server configuration loader."""

import os
import json


def load_mcp_config(*server_names):
    """Load MCP server configs from mcp_config.json.

    Args:
        *server_names: Optional server names to filter. Returns all if none provided.

    Returns:
        Dict of server config(s) keyed by server name.
    """
    config_path = os.path.join(os.path.dirname(__file__), 'mcp_config.json')

    with open(config_path, 'r') as f:
        all_configs = json.load(f)

    if len(server_names) == 0:
        return all_configs

    # Return only the requested server configs that exist in the file
    selected_configs = {}
    for name in server_names:
        if name in all_configs:
            selected_configs[name] = all_configs[name]

    return selected_configs


if __name__ == "__main__":
    print(load_mcp_config('google-calendar'))
