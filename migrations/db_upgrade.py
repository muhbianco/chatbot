import os
import sys
import importlib.util
import asyncio

async def run_up():
    versions_dir = "./versions/"
    files = sorted(os.listdir(versions_dir))
    
    for file_name in files:
        if file_name.endswith(".py"):
            file_path = os.path.join(versions_dir, file_name)
            module_name = os.path.splitext(file_name)[0]
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if hasattr(module, "up"):
                print(f"Running up() method from {file_name}")
                await module.up()

async def run_down():
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
    if len(sys.argv) != 2:
        print("Usage: python db_upgrade.py <up/down>")
        sys.exit(1)
    
    action = sys.argv[1]
    
    if action == "up":
        await run_up()
    elif action == "down":
        await run_down()
    else:
        print("Invalid argument. Use 'up' or 'down'.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())