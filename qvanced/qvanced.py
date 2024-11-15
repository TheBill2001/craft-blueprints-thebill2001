import os
import info
import utils
from pathlib import Path
from Package.CMakePackageBase import CMakePackageBase
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.displayName = "QVanced"
        self.webpage = "https://github.com/TheBill2001/QVanced"
        self.svnTargets["master"] = "https://github.com/TheBill2001/QVanced.git|main"
        self.svnTargets["dev"] = "https://github.com/TheBill2001/QVanced.git|dev"
        self.defaultTarget = "dev"

        # We will move these manually, Craft seem to be messing this up
        self.options.package.movePluginsToBin = False
        self.options.package.moveTranslationsToBin = False

    def setDependencies(self):
        self.buildDependencies["dev-utils/cmake"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None

        self.runtimeDependencies["libs/qt6/qtbase"] = None
        self.runtimeDependencies["libs/qt6/qtdeclarative"] = None

        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kirigami"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None

        self.runtimeDependencies["kde/unreleased/kirigami-addons"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None
        self.runtimeDependencies["kde/frameworks/tier3/qqc2-desktop-style"] = None

        self.runtimeDependencies["kde/plasma/breeze"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        CMakePackageBase.buildTests = False

    @property
    def applicationExecutable(self):
        return "qvanced"

    def createPackage(self):
        if not CraftCore.compiler.isLinux:
            self.ignoredPackages += [
                "libs/dbus",
                "libs/qt6/qtwayland",
                "kde/frameworks/tier1/kdbusaddons",
            ]

        self.defines["shortcuts"] = [
            {"name": self.subinfo.displayName, "target": "bin\qvanced.exe"}
        ]

        self.addExecutableFilter(
            r"(bin|libexec)/(?!(" + self.applicationExecutable + r")).*"
        )
        self.blacklist_file.append(os.path.join(self.blueprintDir(), "blacklist.txt"))

        return super().createPackage()

    def preArchive(self):
        # We will move these manually, Craft seem to be messing this up
        utils.mergeTree(self.archiveDir() / "qml", self.archiveDir() / "bin" / "qml")

        utils.mergeTree(
            self.archiveDir() / "plugins", self.archiveDir() / "bin" / "plugins"
        )

        utils.mergeTree(
            self.archiveDir() / "translations",
            self.archiveDir() / "bin" / "translations",
        )

        return super().preArchive()
