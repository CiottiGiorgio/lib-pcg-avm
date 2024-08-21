import logging
import subprocess
from pathlib import Path
from shutil import rmtree

from smart_contracts.helpers.util import find_app_spec_file

logger = logging.getLogger(__name__)
deployment_extension = "py"


def build(output_dir: Path, contract_path: Path) -> Path:
    output_dir = output_dir.resolve()
    if output_dir.exists():
        rmtree(output_dir)
    output_dir.mkdir(exist_ok=True, parents=True)
    logger.info(f"Exporting {contract_path} to {output_dir}")

    build_result = subprocess.run(
        [
            "algokit",
            "--no-color",
            "compile",
            "python",
            contract_path.absolute(),
            f"--out-dir={output_dir}",
            "--output-arc32",
            # Due to the debug symbols being generated in a way that is dependent on the OS,
            #  we are disabling them for now.
            # This has impacted a CI job making it fail for a very silly reason (forward vs. backward slashes).
            # https://github.com/CiottiGiorgio/lib-pcg-avm/actions/runs/10480295020/job/29027639154
            # FIXME: We probably want to have two sets of TEAL artifacts, one with debug symbols and one without.
            #  The one without debug symbols, can be easily used to detect changes in TEAL in a more
            #  reliable and less noisy way (both by CI and visually).
            #  The one with debug symbols can be used for relating HLL code to TEAL visually.
            "--debug-level=0",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    if build_result.returncode:
        raise Exception(f"Could not build contract:\n{build_result.stdout}")

    app_spec_file_name = find_app_spec_file(output_dir)
    if app_spec_file_name is None:
        raise Exception("Could not generate typed client, .arc32.json file not found")

    # generate_result = subprocess.run(
    #     [
    #         "algokit",
    #         "generate",
    #         "client",
    #         output_dir / app_spec_file_name,
    #         "--output",
    #         output_dir / f"client.{deployment_extension}",
    #     ],
    #     stdout=subprocess.PIPE,
    #     stderr=subprocess.STDOUT,
    #     text=True,
    # )
    # if generate_result.returncode:
    #     if "No such command" in generate_result.stdout:
    #         raise Exception(
    #             "Could not generate typed client, requires AlgoKit 1.1 or "
    #             "later. Please update AlgoKit"
    #         )
    #     else:
    #         raise Exception(
    #             f"Could not generate typed client:\n{generate_result.stdout}"
    #         )
    return output_dir / app_spec_file_name
