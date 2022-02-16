from setuptools import setup

setup(
    name="microwormhole",
    version="0.1",
    packages=["skippytel", "skippytel.commands"],
    include_package_data=True,
    install_requires=[
        "click",
        "adafruit-circuitpython-ssd1306",
        "adafruit-circuitpython-framebuf",
        "adafruit-circuitpython-rfm9x",
        "psutil",
    ],
    entry_points="""
        [console_scripts]
        skippytel=skippytel.cli:cli
    """,
)
