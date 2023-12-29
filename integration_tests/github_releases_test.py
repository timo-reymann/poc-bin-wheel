import platform
import tempfile
from pathlib import Path
from unittest import TestCase

from binary_wheel_builder import Wheel, well_known_platforms, build_wheel
from binary_wheel_builder.api.wheel_sources import GithubReleaseBinarySource
from integration_tests.util import install_wheel, verify_install, verify_wheel_structure


class BufGithubReleaseSource(GithubReleaseBinarySource):
    def __init__(self, version: str):
        super().__init__("bufbuild/buf",
                         version,
                         {
                             well_known_platforms.MAC_SILICONE: "buf-Darwin-arm64",
                             well_known_platforms.MAC_INTEL: "buf-Darwin-x86_64",
                             well_known_platforms.WINDOWS_x86_64: "buf-Windows-x86_64.exe",
                             well_known_platforms.LINUX_GENERIC_x84_64: "buf-Linux-x86_64",
                             well_known_platforms.LINUX_GENERIC_aarch64: "buf-Linux-aarch64",
                             well_known_platforms.LINUX_GENERIC_armv7a: "buf-Linux-aarch64",
                         },
                         "buf/buf")


class DeterministicZipGitHubReleaseSource(GithubReleaseBinarySource):
    def __init__(self, version: str):
        super().__init__("timo-reymann/deterministic-zip",
                         version,
                         {
                             well_known_platforms.MAC_SILICONE: "deterministic-zip_darwin-arm64",
                             well_known_platforms.MAC_INTEL: "deterministic-zip_darwin-amd64",
                             well_known_platforms.LINUX_GENERIC_x84_64: "deterministic-zip_linux-amd64",
                             well_known_platforms.LINUX_GENERIC_aarch64: "deterministic-zip_linux-arm",
                             well_known_platforms.LINUX_GENERIC_armv7a: "deterministic-zip_linux-arm",
                         },
                         "deterministic_zip/deterministic-zip",
                         "")


class GitHubReleasesTest(TestCase):
    def test_buf(self):
        dist_folder = Path(tempfile.mkdtemp())

        for result in build_wheel(
                Wheel(
                    package="buf",
                    executable="buf",
                    name="buf",
                    version="0.0.1",
                    summary='Buf cli wrapped',
                    license='MIT',
                    requires_python=">=3.9",
                    classifier=[
                        'License :: OSI Approved :: MIT License',
                    ],
                    project_urls={
                        'Homepage': 'https://example.com',
                        'Source Code': ' https://github.com/examle/example',
                        'Bug Tracker': ' https://github.com/example/example/issues',
                    },
                    source=BufGithubReleaseSource("1.28.1"),
                    platforms=[
                        well_known_platforms.MAC_INTEL,
                        well_known_platforms.WINDOWS_x86_64,
                        well_known_platforms.MAC_SILICONE,
                        well_known_platforms.LINUX_GENERIC_x84_64,
                    ]
                ),
                dist_folder
        ):
            print(result)
            verify_wheel_structure(
                result.file_path,
                [
                    ('buf-0.0.1.dist-info/RECORD', 0o644),
                    ('buf-0.0.1.dist-info/METADATA', 0o644),
                    ('buf-0.0.1.dist-info/entry_points.txt', 0o644),
                    ('buf/buf', 0o755),
                ]
            )

        install_wheel(dist_folder, "buf")
        verify_install("buf", "--version")



    def test_zip(self):
        dist_folder = Path(tempfile.mkdtemp())
        for result in build_wheel(
                Wheel(
                    package="deterministic_zip",
                    executable="deterministic-zip",
                    name="deterministic-zip",
                    version="0.0.1",
                    summary='deterministic-zip cli wrapped',
                    license='MIT',
                    requires_python=">=3.9",
                    classifier=[
                        'License :: OSI Approved :: MIT License',
                    ],
                    project_urls={
                        'Homepage': ' https://example.com',
                        'Source Code': ' https://github.com/examle/example',
                        'Bug Tracker': ' https://github.com/example/example/issues',
                    },
                    source=DeterministicZipGitHubReleaseSource("2.1.0"),
                    platforms=[
                        well_known_platforms.MAC_INTEL,
                        well_known_platforms.MAC_SILICONE,
                        well_known_platforms.LINUX_GENERIC_x84_64,
                    ]
                ),
                dist_folder
        ):
            print(result)
            verify_wheel_structure(
                result.file_path,
                [
                    ('deterministic_zip-0.0.1.dist-info/RECORD', 0o644),
                    ('deterministic_zip-0.0.1.dist-info/METADATA', 0o644),
                    ('deterministic_zip-0.0.1.dist-info/entry_points.txt', 0o644),
                    ('deterministic_zip/deterministic-zip', 0o755),
                ]
            )

        install_wheel(dist_folder, "deterministic-zip")
        if platform.system() != "Windows":
            verify_install("deterministic-zip", "--version")
