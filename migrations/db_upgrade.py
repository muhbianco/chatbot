import os
import sys
import importlib.util
import asyncio
import asyncmy
import pprint

projeto_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(projeto_dir)

from app.utils.db import DB

db = DB()

class DbUpgrade:

    async def get_schema_version(self) -> int:
        try:
            result = await db.fetchone("SELECT version FROM schema_info")
            return result["version"]
        except asyncmy.errors.ProgrammingError:
            return 0

    async def get_modules_versions(self, action: str, versions_dir: str, current_version: int, target_version: int | None = None) -> list:
        if action == "up":
            files = sorted(os.listdir(versions_dir))
        else:
            files = sorted(os.listdir(versions_dir), reverse=True)
        files = [f for f in files if f.endswith(".py")]
        if action == "up":
            files = [f for f in files if int(f.split(".")[0]) > current_version]
            if target_version:
                files = [f for f in files if int(f.split(".")[0]) <= target_version]
        elif action == "down":
            files = [f for f in files if int(f.split(".")[0]) <= current_version]
            if target_version:
                files = [f for f in files if int(f.split(".")[0]) > target_version]
        return files

    async def save_target_version(self, target_version: int | None):
        if target_version:
            await db.update("UPDATE schema_info SET version=%s", (target_version, ))

    async def run_up(self, target_version: int | None):
        versions_dir = "./versions/"
        current_version = await self.get_schema_version()
        files = await self.get_modules_versions("up", versions_dir, current_version, target_version)
        
        if not files:
            print("Current version", current_version)
            print("No changes to do.")
            return
        
        for ifile, file_name in enumerate(files):
            module_name = os.path.splitext(file_name)[0]
            module_version = int(module_name.split(".")[0])
            file_path = os.path.join(versions_dir, file_name)
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        
            if hasattr(module, "up"):
                print(f"Running up() method from {file_name}")
                await module.up()

        await self.save_target_version(module_version)

    async def run_down(self, target_version: int | None):
        versions_dir = "./versions/"
        current_version = await self.get_schema_version()
        files = await self.get_modules_versions("down", versions_dir, current_version, target_version)

        if not files:
            print("Current version", current_version)
            print("No changes to do.")
            return
        
        for file_name in files:
            module_name = os.path.splitext(file_name)[0]
            module_version = int(module_name.split(".")[0])
            file_path = os.path.join(versions_dir, file_name)
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if hasattr(module, "down"):
                print(f"Running down() method from {file_name}")
                await module.down()

        await self.save_target_version(target_version)

    async def main(self):
        if len(sys.argv) > 3:
            print("Usage: python db_upgrade.py <up/down> <optional: version number>")
            sys.exit(1)
        
        action = sys.argv[1]
        version = None
        if len(sys.argv) > 2:
            try:
                version = int(sys.argv[2])
                print("Target version", version)
            except ValueError as e:
                print("Invalid version number.")
                print(e)
                sys.exit(1)
        
        if action == "up":
            await self.run_up(version)
        elif action == "down":
            await self.run_down(version)
        else:
            print("Invalid argument. Use 'up' or 'down'.")
            sys.exit(1)

if __name__ == "__main__":
    asyncio.run(DbUpgrade().main())