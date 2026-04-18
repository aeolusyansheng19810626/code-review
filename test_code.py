def calculate_area(radius):
    import math
    if radius < 0:
        return "Error"
    return math.pi * radius ** 2

def main():
    r = float(input("Enter radius: "))
    print(calculate_area(r))

if __name__ == "__main__":
    main()
