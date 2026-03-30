from setuptools import setup, find_packages

try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "Akıllı İşletim Sistemi Sınıflandırıcısı (SmartOSOrganizer)"

try:
    with open("requirements.txt", "r", encoding="utf-8") as f:
        requirements = [
            line.split("#")[0].strip() 
            for line in f.read().splitlines() 
            if line.strip() and not line.strip().startswith("#")
        ]
except FileNotFoundError:
    requirements = []

setup(
    name="smartosorganizer",
    version="0.1.0",
    author="Boran Sert",
    description="Yapay zeka destekli, olay güdümlü akıllı dosya sınıflandırıcı aracı.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Boran-Sert/Downloads-Organizer",
    packages=find_packages(exclude=["tests*", "models*"]),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "organizer=smartosorganizer.cli:app",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
)
