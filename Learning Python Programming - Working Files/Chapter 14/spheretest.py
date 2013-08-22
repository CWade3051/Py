#from sphere import *
import sphere

print("Enter the radius of the sphere: ")
radius = int(input())
#print("The area is " + str(area(radius)))
#print("The volume is " + str(volume(radius)))
print("The area is " + str(sphere.area(radius)))
print("The volume is " + str(sphere.volume(radius)))