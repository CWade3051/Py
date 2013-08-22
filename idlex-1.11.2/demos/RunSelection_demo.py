"""
    Run Selection Demo

    Run highlighted code or a single line in the editor with F9.
   
"""

### Demo 1
print('Run a line')     # Place cursor on this line and Press F9.
                        # The executed code highlights.



### Demo 2
for i in range(5):      # Place cursor on this line and Press F9.
                        # A list of numbers will print. 

    print(i)            # Place cursor on this line and Press F9.
                        # The print function will still execute

    print(i**2)

### Tag Region Demo


# Highlight the following lines and press Ctrl+J to Tag
# To untag a line, use Ctrl+K

a = [1, 2, 3, 4, 5]
for i in a:
    print(i)

# Place the cursor in this region an press Ctrl+F9 to run it.




