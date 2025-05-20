from .server import serve

def main():
    """MCP D-Wave Server - Quantum computing functionality for MCP"""
    import argparse
    import asyncio

    parser = argparse.ArgumentParser(
        description="Give a model the ability to interact with D-Wave quantum computers"
    )
    parser.add_argument("--use-simulator", action="store_true", help="Use D-Wave simulator instead of real hardware", default=True)
    
    args = parser.parse_args()
    asyncio.run(serve(use_simulator=args.use_simulator))


if __name__ == "__main__":
    main() 