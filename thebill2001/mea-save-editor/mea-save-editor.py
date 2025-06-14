import os
import info
import utils
from Package.CMakePackageBase import CMakePackageBase
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.displayName = "Mass Effect: Andronmeda Save Editor"
        self.webpage = "https://github.com/TheBill2001/mea-save-editor"
        self.svnTargets["master"] = "https://github.com/TheBill2001/mea-save-editor.git|main"
        self.defaultTarget = "master"

        if CraftCore.compiler.isWindows:
            # We will move these manually
            self.options.package.movePluginsToBin = False
            self.options.package.moveTranslationsToBin = False

    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.Windows | CraftCore.compiler.Platforms.Linux

    def setDependencies(self):
        self.buildDependencies["dev-utils/cmake"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None

        self.runtimeDependencies["libs/zlib"] = None

        self.runtimeDependencies["libs/qt6/qtbase"] = None
        self.runtimeDependencies["libs/qt6/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt6/qtsvg"] = None

        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kirigami"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None
        self.runtimeDependencies["kde/frameworks/tier3/qqc2-desktop-style"] = None
        self.runtimeDependencies["kde/unreleased/kirigami-addons"] = None

        # Kirigami Addons need this
        self.runtimeDependencies["kde/frameworks/tier1/kitemmodels"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        CMakePackageBase.buildTests = False

    @property
    def applicationExecutable(self):
        return "mea-save-editor"

    def createPackage(self):
        self.ignoredPackages += [
            "kde/frameworks/tier1/kcodecs",
            "kde/frameworks/tier2/kdoctools",
            "kde/frameworks/tier2/kwidgetsaddons",
            "libs/cups",
            "libs/dbus",
            "libs/ffmpeg",
            "libs/glib",
            "libs/libjpeg-turbo",
            "libs/libxml2",
            "libs/sqlite",
            "libs/libunistring"
        ]

        if CraftCore.compiler.isWindows:
            self.ignoredPackages += [
                "libs/qt6/qtwayland"
            ]

        self.defines["shortcuts"] = [
            {"name": self.subinfo.displayName, "target": f"bin/{self.applicationExecutable}.exe"}
        ]

        self.addExecutableFilter(fr"bin/(?!({self.applicationExecutable})).*")

        self.blacklist_file.append(os.path.join(self.blueprintDir(), "blacklist.txt"))
        if CraftCore.compiler.isWindows:
            self.blacklist_file.append(os.path.join(self.blueprintDir(), "blacklist-windows.txt"))

        return super().createPackage()

    def preArchive(self):
        # We will move these manually, Craft seem to be messing this up
        utils.mergeTree(self.archiveDir() / "bin", self.archiveDir())
        return super().preArchive()
