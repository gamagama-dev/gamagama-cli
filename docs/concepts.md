# Core Concepts

gamagama-cli is built around a few core concepts that differentiate it from standard CLI tools.

## The Tree

Everything in gamagama-cli is a **Node** in a **Tree**.

*   **Root**: The top-level container.
*   **Branches**: Nodes that contain other nodes (like folders).
*   **Leaves**: Nodes that contain data (like files).

## Navigation

You are always located at a specific node in the tree, called the **Current Node**.

*   When you type a command, it is executed in the context of your Current Node.
*   You can move up and down the tree to change your context.

## Command Bubbling

If you try to run a command that doesn't exist on your Current Node, gamagama-cli looks up the tree (to the parent, then the grandparent, etc.) until it finds a handler.

This allows global commands (like `quit` or `roll`) to work everywhere, while specific commands (like `add player`) only work when you are in the correct location.
