import io
from base64 import b64decode, b64encode
from pathlib import Path
from signal import SIG_DFL, SIGINT, signal
from typing import Any

import zmq
from PIL import Image as im
from PIL.Image import Image

"""
Tests to write...
- invalid hex colors values
- valid hex colors
    - # prefixed
    - non-# prefixed
    - mixed prefices
- missing one color/property
"""

# assuming we're at the project root
# test_image = Path.cwd() / "tests" / "last_recieved_test_image.png"
test_image = Path.cwd() / "tests" / "good_dog.png"


def print_response(response: dict[str, str]):
    print("{")
    for key, value in response.items():
        if len(value) > 50:
            value = value[0:50] + " (truncated)"
        print(f"    {key}: {value}")
    print("}")


def main() -> None:
    # maybe use argparser or something for host, port, etc

    host = "localhost"
    port = "8675"

    # please exit when someone presses ctrl+C
    signal(SIGINT, SIG_DFL)

    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(f"tcp://{host}:{port}")
    print(f"connected to service at tcp://{host}:{port}")

    print(f"reading image file: {test_image}")
    with open(test_image, "rb") as f:
        data = f.read()
        b64data = b64encode(data).decode("ascii")
        print(f"sending {str(b64data[0:10])}... image")
        socket.send_json({"image": b64data, "intensity": 1})

    response: Any = socket.recv_json()

    # print("recieved response: ", response)

    print_response(response)

    if response["status"] == "ok":
        img = response["image"]
        img_bytes = b64decode(img)

        parent_folder = Path(__file__).parent.resolve()
        with open(parent_folder / "last_recieved_test_image.png", "wb") as f:
            f.write(img_bytes)

        img_bio = io.BytesIO(img_bytes)
        i: Image = im.open(img_bio)
        i.show()


if __name__ == "__main__":
    main()
