# Write a program that accepts two lines (x1,x2) and (x3,x4) on
# the x-axis and returns whether they overlap. As an example, (1,5)
# and (2,6) overlaps but not (1,5) and (6,8).

def check_overlap(x1, x2, x3, x4):
    if min(x3, x4) >= max(x1, x2) or max(x3, x4) <= min(x1, x2):
        return False
    return True


line_coords = []
coord_counter = 0

while coord_counter < 4:
    try:
        coord = int(input(f"Enter x{coord_counter + 1} : "))
    except ValueError:
        print("Please enter an integer! Try again.")
        continue
    else:
        line_coords.append(coord)
        coord_counter += 1

if check_overlap(*line_coords):
    print(
        f"Lines ({line_coords[0]}, {line_coords[1]}) and ({line_coords[2]}, {line_coords[3]}) overlap")
else:
    print(
        f"Lines ({line_coords[0]}, {line_coords[1]}) and ({line_coords[2]}, {line_coords[3]}) do not overlap")
