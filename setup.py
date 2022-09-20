from setuptools import find_packages, setup

setup(
    name="place-explorer",
    version="0.1",
    description="A python package for obtaining places via Google Maps API.",
    author="Taichi Uchio, Naoki Kiyohara",
    url="https://github.com/TUCHIO/PlaceExplorer",
    license="MIT License",
    install_requires=["numpy", "pandas", "matplotlib", "googlemaps"],
    packages=find_packages(),
)
