# Test linter
# function with at least 5 style-related issues and at least 5 logic / code-quality issues

def calculate_area( radius ):   # extra spaces in params (style)
    pi=3.14  # missing spaces around operator (style)
    area = pi * radius ** 2
    unused_var = 10  # unused variable (code quality)
    if radius < 0:
        print("invalid radius")  # side effect instead of handling properly (logic)
    return area
    print("this will never run")  # unreachable code (logic)


if __name__=="__main__":  # missing spaces around operator (style)
    r=5   # missing spaces (style)
    area = calculate_area(r)

    if r == 5:
        pass  # unnecessary pass (code quality)

    if r > 0:
        if r > 1:  # redundant nested condition (logic)
            print("radius is positive")

    print("The area of the circle with radius "+str(r)+" is: "+str(area))  # bad string formatting (style)
    print("The area is: {}".format(area))  # inconsistent formatting style (style)

    calculate_area("five")  # wrong type (logic)