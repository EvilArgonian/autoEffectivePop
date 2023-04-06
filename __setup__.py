import setuptools

with open("README.md", "r", encoding="utf-8") as fhand:
    long_description = fhand.read()

setuptools.setup(
    name="sung-lab-autoEffPop",
    version="0.0.1",
    author="Perrin Mele",
    author_email="pmele@uncc.edu",
    description="A pipeline for determining nucleotide diversity estimators of bacterial species.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EvilArgonian/autoEffectivePop",
    project_urls={
        "Bug Tracker": "https://github.com/EvilArgonian/autoEffectivePop/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: ? :: ?",
        "Operating System :: POSIX :: Linux",
    ],
    install_requires=["dendropy"],
    packages=setuptools.find_packages(),
    python_requires=">=2.7.15",
    entry_points={
        "console_scripts": [
            "myProgramNameHere = __main__:main",
        ]
    }
)
