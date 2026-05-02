import subprocess
import os

def decrypt_auto(input_file, passphrase):
    output_file = input_file.replace(".gpg", "")

    with open(output_file, "wb") as f:
        subprocess.run(
            [
                "gpg",
                "--batch",
                "--yes",
                "--pinentry-mode", "loopback",
                "--passphrase", passphrase,
                "--decrypt",
                input_file
            ],
            stdout=f,
            check=True
        )

    return output_file