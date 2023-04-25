with open("./VERSION", "r") as _version:
    # during default, this does nothing
    # during release, this will be replaced before the run with a proper version
    VERSION = _version.readline().strip()

python_sources(
    name="root",
)

python_requirements(
    name="requirements",
    module_mapping={
        "injective-py": ["pyinjective"],
    }
)

python_distribution(
    name="distribution",
    dependencies=[
        "//:requirements",
        "//:root",
    ],
    generate_setup=True,
    entry_points={
        "console_scripts": {
            # needed so pants actually detects files to add
            "_fake": "frontrunner_sdk:_fake",
        },
    },
    repositories=["@deploy"],
    provides=python_artifact(
        name="frontrunner-sdk",
        version=VERSION,
        description="Frontrunner SDK",
        license="Apache-2.0",
        author="Frontrunner",
        author_email="support@getfrontrunner.com",
        url="https://github.com/GetFrontrunner/frontrunner-sdk",
        python_requires=">=3.8,<4",
        classifiers=[
            # https://pypi.org/classifiers/
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: Apache Software License",
            "Natural Language :: English",
            "Topic :: Games/Entertainment",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
        ],
    ),
)

__defaults__({
    python_tests: dict(dependencies=["//:requirements"])
})
