import platform
import sys
import pathlib
import os

_lib_root = os.environ.get("KCL_LIB_ROOT")
if _lib_root:
    LIB_ROOT = pathlib.Path(_lib_root)
else:
    # Test Lib ROOT
    TEST_LIB_ROOT = pathlib.Path(__file__).parent.parent.parent.parent
    LIB_ROOT = TEST_LIB_ROOT
    if not TEST_LIB_ROOT.joinpath("lib").exists():
        LIB_ROOT = pathlib.Path(__file__).parent.parent


def is_amd64_arch():
    return platform.machine() in ["x86_64", "amd64", "AMD64"]


if sys.platform == "darwin":
    if is_amd64_arch():
        with open(f"{LIB_ROOT}/lib/darwin-amd64/libkclvm_cli_cdylib.dylib", "rb") as f:
            DARWIN_AMD64_CLI_LIB = f.read()
    else:
        with open(f"{LIB_ROOT}/lib/darwin-arm64/libkclvm_cli_cdylib.dylib", "rb") as f:
            DARWIN_ARM64_CLI_LIB = f.read()

    def cli_lib():
        return DARWIN_AMD64_CLI_LIB if is_amd64_arch() else DARWIN_ARM64_CLI_LIB

elif sys.platform.startswith("linux"):
    if is_amd64_arch():
        with open(f"{LIB_ROOT}/lib/linux-amd64/libkclvm_cli_cdylib.so", "rb") as f:
            LINUX_AMD64_CLI_LIB = f.read()
    else:
        with open(f"{LIB_ROOT}/lib/linux-arm64/libkclvm_cli_cdylib.so", "rb") as f:
            LINUX_ARM64_CLI_LIB = f.read()

    def cli_lib():
        return LINUX_AMD64_CLI_LIB if is_amd64_arch() else LINUX_ARM64_CLI_LIB

elif sys.platform == "win32":
    if is_amd64_arch():
        with open(f"{LIB_ROOT}/lib/windows-amd64/kclvm_cli_cdylib.dll", "rb") as f:
            WINDOWS_AMD64_CLI_LIB = f.read()
        with open(f"{LIB_ROOT}/lib/windows-amd64/kclvm_cli_cdylib.lib", "rb") as f:
            WINDOWS_AMD64_EXPORT_LIB = f.read()
    else:
        with open(f"{LIB_ROOT}/lib/windows-arm64/kclvm_cli_cdylib.dll", "rb") as f:
            WINDOWS_ARM64_CLI_LIB = f.read()
        with open(f"{LIB_ROOT}/lib/windows-arm64/kclvm_cli_cdylib.lib", "rb") as f:
            WINDOWS_ARM64_EXPORT_LIB = f.read()

    def cli_lib():
        return WINDOWS_AMD64_CLI_LIB if is_amd64_arch() else WINDOWS_ARM64_CLI_LIB

    def export_lib():
        return WINDOWS_AMD64_EXPORT_LIB if is_amd64_arch() else WINDOWS_ARM64_EXPORT_LIB

else:
    raise f"Unsupported platform {sys.platform}, expected win32, linux or darwin platform"