def attempt(command):
    try:
        command #type: ignore
    except:
        print('command failed')

l = [1, 2, 3, 4]

attempt(print(l[8]))