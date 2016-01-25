def ModelIt(fromUser = 'Default',births=[]):
    in_month = len(births)
    print 'the number born is %i' % in_month
    result = in_month
    if fromUser != 'Default':
        return result
    else:
        return 'check your input!'
