from setuptools import setup, find_packages

setup(
    name="rscp-protobuf",
    version="VERSION_PLACEHOLDER",
    packages=find_packages(),
    install_requires=[
        "protobuf>=3.0.0",
    ],
    package_data={
        "rscp_protobuf": ["*.py"],
    },
    include_package_data=True,
)
