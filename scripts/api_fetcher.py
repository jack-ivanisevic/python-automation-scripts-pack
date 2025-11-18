import time
from typing import Any, Dict, Optional

import requests


class APIFetchError(Exception):
    """Custom exception for API fetch errors."""
    pass


def fetch_with_retries(
    url: str,
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, Any]] = None,
    max_retries: int = 3,
    backoff_seconds: int = 2,
    timeout_seconds: int = 10,
) -> Dict[str, Any]:
    """
    Fetch JSON data from an API endpoint with basic retry logic.

    This utility:
    - Sends a GET request to the provided URL
    - Retries on network/5xx errors
    - Uses exponential backoff between attempts
    - Returns parsed JSON on success

    It is designed as a generic pattern that can be adapted to many APIs.
    No real credentials are used here; in practice you would inject headers,
    tokens, or API keys through environment variables or config.
    """
    attempt = 0

    while attempt <= max_retries:
        try:
            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=timeout_seconds,
            )

            # Raise an HTTPError for bad responses (4xx/5xx)
            response.raise_for_status()

            # Attempt to parse JSON
            data = response.json()
            return data

        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            # Network-related error, consider retry
            attempt += 1
            if attempt > max_retries:
                raise APIFetchError(
                    f"Failed to fetch {url} after {max_retries} retries due to network error: {e}"
                )
            sleep_for = backoff_seconds * attempt
            print(f"Network error on attempt {attempt} for {url}. Retrying in {sleep_for} seconds...")
            time.sleep(sleep_for)

        except requests.exceptions.HTTPError as e:
            # For 4xx/5xx, decide what you want to do
            status_code = e.response.status_code if e.response is not None else "unknown"
            raise APIFetchError(f"HTTP error {status_code} while fetching {url}: {e}") from e

        except ValueError as e:
            # JSON decode issue
            raise APIFetchError(f"Failed to parse JSON response from {url}: {e}") from e


def example_usage() -> None:
    """
    Example usage of fetch_with_retries.

    Note:
    - This uses a placeholder public API.
    - Replace `url` with a real endpoint (e.g., a public test API) when testing.
    - Do not hardcode real API keys; pass them via environment variables or config.
    """
    url = "https://api.example.com/data"  # Placeholder URL
    headers = {
        # "Authorization": "Bearer YOUR_TOKEN_HERE",  # Do not hardcode real tokens in production
    }
    params = {
        "example_param": "value"
    }

    try:
        data = fetch_with_retries(url, headers=headers, params=params)
        print("Received data:")
        print(data)
    except APIFetchError as e:
        print(f"API fetch failed: {e}")


if __name__ == "__main__":
    example_usage()
