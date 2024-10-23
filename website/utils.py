import math

# Function to calculate user level based on total questions solved
def calculate_level(total_solved):
    if total_solved == 0:
        #  Return level 1 if total answer is 0
        return 1
    else:
        # Return log base 2 value of total solved rounded down (floored)
        return math.floor(math.log(total_solved, 2)) + 1