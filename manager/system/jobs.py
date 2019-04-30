class BaseJob:
    name = ""

    def __init__(self, manager):
        self.manager = manager

    async def execute(self):
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

    async def execute(self):
        await self.manager.download_and_install_package(self.reference)


class InstallPackage(PackageJob):
    name = "Install package"

    async def execute(self):
        await self.manager.install_package(self.reference)


class UninstallPackage(PackageJob):
    name = "Uninstall package"

    async def execute(self):
        await self.manager.uninstall_package(self.reference)


class DeletePackage(PackageJob):
    name = "Delete package"

    async def execute(self):
        await self.manager.delete_package(self.reference)
