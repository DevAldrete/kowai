#!/bin/bash

echo "Installing runtime dependencies..."
pnpm install bcrypt jsonwebtoken pg

echo "Installing development dependencies..."
pnpm install -D @types/bcrypt @types/jsonwebtoken @types/pg jest @types/jest ts-jest @playwright/test

echo "Checking AnalogJS dependencies for testing..."
# Check if @analogjs/platform is in package.json, if not, consider adding it or specific testing utilities.
# For now, assume core testing setup will be handled in the next step.
if ! grep -q "@analogjs/platform" package.json; then
  echo "@analogjs/platform not found, ensure your project is correctly set up for testing with AnalogJS."
  echo "Installing @analogjs/platform..."
  pnpm install @analogjs/platform
  echo "Installation of @analogjs/platform complete."
fi

echo "Installation complete. Review package.json for changes."
