def API_Read_Safe(url, timeout=5, attempts=3):
    """Read API URL, handle HTTP 429 and timeout errors"""

    tries = 0

    while tries < attempts:
        tries += 1

        try:
            # read target URL

            response = requests.get(url, headers=headers, timeout=timeout)

            # if successful, return the response

            if response.ok:
                print("Completed successfully")

                return response

            # If response is not "ok", handle error code 429:

            # - wait "Retry-After" seconds or 1 sec, if not present

            # - retry

            if response.status_code == 429:
                try:
                    retry_after = int(response.headers.get("Retry-After"))

                except Exception:
                    retry_after = 1

                print(f"Retry after {retry_after} seconds")

                sleep(retry_after)

                continue

            # if not OK and not 429, then it's something unrecoverable

            print(f"HTTP error: {response.status_code}")

            response.raise_for_status()

        ## if timeout error, retry. If any other error, leave it unhandled

        except requests.exceptions.ConnectTimeout:
            print("Timeout, retry")

            continue

    # return "None" if unsuccessful after all attempts

    print("Unable to get any response")

    return None
