#   string formatting with  %
#   %[+,-][0][w][.n][type]


print('%s buys %d apples' % ('Mike', 5))



#str
print('%s' % ('hello'))
print('|%s|' % ('hello'))
print('|%20s|' % ('hello')) #deault right aligned
print('|%+20s|' % ('hello'))
print('|%-20s|' % ('hello')) # left aligned
print('|%+020s|' % ('hello'))

print('|%20.2s|' % ('hello'))
#int
print('|%d|' % (15))
print('|%20d|' % (15))
print('|%+20d|' % (15))
print('|%-20d|' % (15))
print('|%020d|' % (15))
print('|%20.2d|' % (15))

#float
print('|%f|' % (123456.789))
print('|%.2f|' % (123456.789))
print('|%.2f|' % (123456.781))
print('|%20.2f|' % (123456.781))
print('|%20s|' % format(123456.781, ','))


# string formatting with string.format function

# {[index,key]:[[fill] alignment] [+,-,' '][#][0][w][group][.n][type]}

#string
print('|{}|'.format('hello'))
print('|{:s}|'.format('hello'))
print('|{:20s}|'.format('hello')) #default left  aligned
print('|{:>20s}|'.format('hello'))
print('|{:<20s}|'.format('hello'))
print('|{:^20s}|'.format('hello'))
print('|{:-^20s}|'.format('hello'))
print('|{:*^20s}|'.format('hello'))
print('|{:*^20.2s}|'.format('hello'))

#int
print('|{}|'.format(15))
print('|{:d}|'.format(15))
print('|{:20d}|'.format(15)) # default right aligned
print('|{:<20d}|'.format(15))
print('|{:^20d}|'.format(15))
print('|{:*^20d}|'.format(15))

print('|{:+d}|'.format(15))
print('|{:+d}|'.format(-15))

print('|{:-d}|'.format(15))
print('|{:-d}|'.format(-15))

print('|{: d}|'.format(15))
print('|{: d}|'.format(-15))


#type s d x o b
print('|{:d}|'.format(15))
print('|{:x}|'.format(15))
print('|{:o}|'.format(15))
print('|{:b}|'.format(15))

print('|{:#d}|'.format(15))
print('|{:#x}|'.format(15))
print('|{:#o}|'.format(15))
print('|{:#b}|'.format(15))

print('|{:020d}|'.format(15))


#float
print('|{:f}|'.format(123456.789))
print('|{:20f}|'.format(123456.789))
print('|{:20.2f}|'.format(123456.789))
print('|{:20.2f}|'.format(123456.781))


print('|{:20,.2f}|'.format(123456.781))
print('|{:20_.2f}|'.format(123456.781))

#index and key

print('|{},{},{}|'.format(1, 2, 3))
print('|{0},{1},{2}|'.format(1, 2, 3))
print('|{0},{1},{0}|'.format(1, 2))
print('|{0},{1},{1}|'.format(1, 2))

print('{} buys {} apples'.format('Mike', 5))
print('{0} buys {1} apples'.format('Mike', 5))
print('{name} buys {amount} apples'.format(name='Mike', amount=5))
print('|{name:^20s}| buys {amount:#x} apples'.format(name='Mike', amount=15))