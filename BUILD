python_sources(
    name="root",
)

python_requirements(
    name="requirements",
    module_mapping={
        "injective-py": ["pyinjective"],
    }
)

__defaults__({
    python_tests: dict(dependencies=["//:requirements"])
})
