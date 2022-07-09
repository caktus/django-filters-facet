import setuptools

if __name__ == "__main__":
    setuptools.setup(
        name="django_filters_facet",  # without the name the package is installed as UNKNOWN
        packages=["django_filters_facet"],
        package_dir={"": "src"},
    )
