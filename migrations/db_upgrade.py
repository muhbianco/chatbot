import os
import sys
import importlib.util
import asyncio
import asyncmy

projeto_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(projeto_dir)

from app.utils.db import DB

db = DB()

async def get_schema_version():
    try:
        result = await db.fetchone("SELECT version FROM schema_info")
        return result[0]
    except asyncmy.errors.ProgrammingError:
        return 0

async def run_up(version: int):
    versions_dir = "./versions/"
    files = sorted(os.listdir(versions_dir))
    actual_version = await get_schema_version()
    files = []
    print("actual_version", actual_version)
    print("migration version", version)


    
    for ifile, file_name in enumerate(files):
        if file_name.endswith(".py"):
            module_name = os.path.splitext(file_name)[0]
            module_version = int(module_name.split(".")[0])
            file_path = os.path.join(versions_dir, file_name)
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        
            if hasattr(module, "up"):
                print(f"Running up() method from {file_name}")
                await module.up()

async def run_down(version: int):
    versions_dir = "versions/"
    files = sorted(os.listdir(versions_dir), reverse=True)
    
    for file_name in files:
        if file_name.endswith(".py"):
            file_path = os.path.join(versions_dir, file_name)
            module_name = os.path.splitext(file_name)[0]
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if hasattr(module, "down"):
                print(f"Running down() method from {file_name}")
                await module.down()

async def main():
    if len(sys.argv) > 3:
        print("Usage: python db_upgrade.py <up/down> <optional: version number>")
        sys.exit(1)
    
    action = sys.argv[1]
    version = None
    if len(sys.argv) > 2:
        try:
            version = int(sys.argv[2])
            print("version", version)
        except ValueError as e:
            print("Invalid version number.")
            print(e)
            sys.exit(1)
    
    if action == "up":
        await run_up(version)
    elif action == "down":
        await run_down(version)
    else:
        print("Invalid argument. Use 'up' or 'down'.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())