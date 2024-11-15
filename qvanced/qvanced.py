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
            self.ignoredPackages += ["libs/dbus", "libs/qt6/qtwayland"]

        self.ignoredPackages += [
            "libs/qt6/qt5compat",
            "libs/qt6/qttools",
            "libs/qt6/qtlanguageserver",
            "libs/qt/qtmultimedia",
            "libs/cups",
            "kde/frameworks/tier1/kdbusaddons",
            "kde/frameworks/tier3/kcmutils",
            "kde/frameworks/tier1/kwidgetsaddons",
            "kde/frameworks/tier3/kconfigwidgets",
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
        utils.mergeTree(Path(self.archiveDir()) / "bin", self.archiveDir())

        return super().preArchive()
