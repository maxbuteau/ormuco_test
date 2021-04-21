# Write a software library that accepts 2 version string as input and returns
# whether one is greater than, equal, or less than the other.
# As an example: “1.2” is greater than “1.1”.
# Please provide all test cases you could think of.

# I assumed that the version strings are a series of positive integers separated by '.'
# For example, version 1.1.2
# My function returns 1 if version 1 is greater than version 2, 0 if they are equal
# and -1 if version 2 is greater than version 1

def compare_versions(v1, v2):
    # Get 2 lists with the numbers without the '.'
    l1 = v1.split('.')
    l2 = v2.split('.')

    # Append 0's to the shorter version string
    if len(l1) > len(l2):
        l2.extend(["0"] * (len(l1) - len(l2)))
    elif len(l2) > len(l1):
        l1.extend(["0"] * (len(l2) - len(l1)))

    # Compare each number of both versions
    for i in range(len(l1)):
        if not l1[i].isnumeric() or not l2[i].isnumeric():
            raise ValueError("Invalid version format")
        if int(l1[i]) < 0 or int(l2[i]) < 0:
            raise ValueError("Version cannot be negative")

        if int(l1[i]) > int(l2[i]):
            return 1
        elif int(l2[i]) > int(l1[i]):
            return -1

    # The versions are equal
    return 0
