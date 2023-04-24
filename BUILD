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
            # needed so pants actually detects files to add; otherwise it's
            # empty :-(
            "_fake": "frontrunner_sdk:_fake",
        },
    },
    repositories=["@deploy"],
    provides=python_artifact(
        name="frontrunner-sdk",
        version="0.0.1",
        description="Frontrunner SDK",
        license="Apache-2.0",
        author="Frontrunner",
        author_email="support@getfrontrunner.com",
        url="https://github.com/GetFrontrunner/frontrunner-sdk",
        python_requires=">=3.8,<4",
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Financial and Insurance Industry",
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
