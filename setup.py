from setuptools import find_packages, setup


setupdict = {
    "name": "pf",
    "version": "0.0.0",
    "packages": find_packages(),
    "include_package_data": True,
    "install_requires": ["websockets", "bson"],
}
if __name__ == "__main__":
    setup(**setupdict)
