from setuptools import find_packages, setup

PACKAGE_NAME = "nrai_pathplanning"

setup(
    name=PACKAGE_NAME,
    version="0.0.1",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + PACKAGE_NAME]),
        ("share/" + PACKAGE_NAME, ["package.xml"]),
    ],
    install_requires=["setuptools", "numpy>=2.2.6"],
    zip_safe=True,
    maintainer="Newcastle Racing AI",
    description="Newcastle Racing AI module for path planning",
    license="MIT",
    extras_require={
        "test": [
            "pytest",
        ],
        "standalone": [
            "nrai_rosutils @ git+https://github.com/NewcastleRacingAI/nrai_rosutils.git",
        ],
    },
    entry_points={
        "console_scripts": [
            "nrai_pathplanning = nrai_pathplanning.__main__:main",
            "ros_node = nrai_pathplanning.ros:main",
        ],
    },
)
