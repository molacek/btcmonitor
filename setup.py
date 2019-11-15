import setuptools

with open("README.md", 'r') as fh:
    long_description = fh.read()


setuptools.setup(
    name="btcmonitor",
    version="0.0.6",
    author="Lukáš Moláček",
    author_email="lukas@molacek.net",
    packages=setuptools.find_packages(),
    install_requires=["xdg", "requests", "svgwrite"],
    entry_points={
        "console_scripts": [
            "get_btc_price = btcmonitor:main"
        ]
    }
)
