def palindrome_check(palindrome):
#name of the function
    string = palindrome
    # removing undesired characters 
    string = string.replace(' ','')
    string = string.lower()
    #strating the pointers
    left = 0
    right = len(string)-1
    #checking the string for palidrome
    while left < right:
        if string[left] != string[right]:
            return "no"
        left += 1
        right -= 1
        if left >= right:
            return "yes"
a = palindrome_check('no lemon, no melon')
print(a)