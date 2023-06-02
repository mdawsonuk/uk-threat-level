from setuptools import find_packages, setup

LONG_DESC = open("README.md").read()
PACKAGES = find_packages(exclude=["tests", "tests.*"])
REQUIREMENTS = list(val.strip() for val in open("requirements.txt"))
MIN_PY_VERSION = "3.9"

setup(
    name="uk_threat_level",
    version="0.1.0",
    license="MIT License",
    url="https://github.com/mdawsonuk/uk-threat-level/",
    author="Matt Dawson",
    author_email="matt@mdawson.dev",
    description="Python package to get the current UK Threat Level from JTAC/MI5",
    long_description=LONG_DESC,
    long_description_content_type="text/markdown",
    packages=PACKAGES,
    zip_safe=True,
    platforms="any",
    install_requires=REQUIREMENTS,
    python_requires=f">={MIN_PY_VERSION}",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)