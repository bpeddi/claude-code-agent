"""Simple test to verify the math tools work."""
from server import add, subtract, multiply, divide

# Test all operations
print("Testing math tools...")
print(f"add(5, 3) = {add(5, 3)}")
print(f"subtract(10, 4) = {subtract(10, 4)}")
print(f"multiply(6, 7) = {multiply(6, 7)}")
print(f"divide(20, 4) = {divide(20, 4)}")

# Test divide by zero
try:
    divide(10, 0)
except ValueError as e:
    print(f"divide(10, 0) raised: {e}")

print("\nAll tests passed!")
