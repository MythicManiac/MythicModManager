class BaseJob:
    name = ""

    def __init__(self, manager):
        self.manager = manager

    async def execute(self, progress):
        pass

    @property
    def parameters_str(self):
        return ""


class PackageJob(BaseJob):
    def __init__(self, manager, reference):
        super().__init__(manager)
        self.reference = reference

    @property
    def parameters_str(self):
        return str(self.reference)


class DownloadAndInstallPackage(PackageJob):
    name = "Download and install package"

    async def execute(self, progress):
        await self.manager.download_and_install_package(self.reference, progress)


class InstallPackage(PackageJob):
    name = "Install package"

    async def execute(self, progress):
        await self.manager.install_package(self.reference, progress)


class UninstallPackage(PackageJob):
    name = "Uninstall package"

    async def execute(self, progress):
        await self.manager.uninstall_package(self.reference)


class DeletePackage(PackageJob):
    name = "Delete package"

    async def execute(self, progress):
        await self.manager.delete_package(self.reference)
