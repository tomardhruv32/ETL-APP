import os
import subprocess
from pathlib import Path

# ============================================================
# Apache Hop configuration
# ============================================================

# Project folder.
PROJECT_HOME = Path(__file__).resolve().parent

# Apache Hop installation folder
HOP_HOME = PROJECT_HOME / "hop"

# Hop workflow file
WORKFLOW_FILE = PROJECT_HOME / "workflow.hwf"


# ============================================================
# Start Apache Hop workflow
# ============================================================

def start_hop_workflow():
    # Select runner based on Operating System
    if os.name == "nt":
        hop_run = HOP_HOME / "hop-run.bat"
    else:
        hop_run = HOP_HOME / "hop-run.sh"

    # Check whether Apache Hop script exists
    if not hop_run.exists():
        raise FileNotFoundError(
            f"Apache Hop runner not found at:\n{hop_run}"
        )

    # Check whether workflow exists
    if not WORKFLOW_FILE.exists():
        raise FileNotFoundError(
            f"Workflow file not found:\n{WORKFLOW_FILE}"
        )

    print("=" * 70)
    print("Starting Apache Hop workflow...")
    print(f"Project:  {PROJECT_HOME}")
    print(f"Hop:      {hop_run}")
    print(f"Workflow: {WORKFLOW_FILE}")
    print("=" * 70)

    # Run Apache Hop workflow
    # shell=True ensures Windows executes batch files correctly via cmd.exe
    result = subprocess.run(
        [
            str(hop_run),
            "-f",
            str(WORKFLOW_FILE)
        ],
        cwd=str(PROJECT_HOME),
        shell=(os.name == "nt"),
        check=False
    )

    # Check result
    if result.returncode == 0:
        print("\nApache Hop workflow completed successfully.")
    else:
        print(
            f"\nApache Hop workflow failed."
            f"\nExit code: {result.returncode}"
        )

    return result.returncode


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":
    start_hop_workflow()