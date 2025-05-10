from django.core.management.utils import get_random_secret_key

# Generate the secret key
secret_key = get_random_secret_key()

# Define the text to be centered
text = f"SECRET_KEY: {secret_key}"

# Define the width of the border
border_width = len(text) + 8  # Adjust the padding as needed

# Print the top border
print('#' * border_width)

# Print the centered text with '#' padding
print(f"#{text.center(border_width - 2)}#")

# Print the bottom border
print('#' * border_width)
