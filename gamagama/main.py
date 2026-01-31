def run():
    """Main entry point for the gamagama CLI."""
    print("Welcome to gamagama!")
    print("Type 'quit' to exit.")

    while True:
        try:
            command = input("gg> ")
            if command.lower() == 'quit':
                break
            # TODO: Process the command
            print(f"Unknown command: {command}")
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

if __name__ == "__main__":
    run()
