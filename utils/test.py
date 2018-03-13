onegin = open('../onegin.txt', encoding='utf-8').readlines()
onegin = filter(lambda x: 50 > len(x.strip()) > 10, onegin)
onegin = [s.strip() for s in onegin]

print(*onegin[:100], sep='\n')