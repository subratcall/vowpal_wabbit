import pyvw


def my_predict(vw, ex):
    pp = 0.
    for f,v in ex.iter_features():
        pp += vw.get_weight(f) * v
    return pp

def ensure_close(a,b,eps=1e-6):
    if abs(a-b) > eps:
        raise Exception("test failed: expected " + str(a) + " and " + str(b) + " to be " + str(eps) + "-close, but they differ by " + str(abs(a-b)))

###############################################################################3
vw = pyvw.vw("--quiet")


###############################################################################3
vw.learn("1 |x a b")


###############################################################################3
print '# do some stuff with a read example:'
ex = pyvw.example(vw, "1 |x a b |y c")
ex.learn() ; ex.learn() ; ex.learn() ; ex.learn()
updated_pred = ex.get_updated_prediction()
print 'current partial prediction =', updated_pred

# compute our own prediction
print '        my view of example =', str(list(ex.iter_features()))
my_pred = my_predict(vw, ex)
print '     my partial prediction =', my_pred
ensure_close(updated_pred, my_pred)
print ''
ex.finish()

###############################################################################3
print '# make our own example from scratch'
ex = pyvw.example(vw)
ex.set_label_string("0")
ex.push_features('x', ['a', 'b'])
ex.push_features('y', [('c', 1.)])
ex.setup_example()

print '        my view of example =', str(list(ex.iter_features()))
my_pred2 = my_predict(vw, ex)
print '     my partial prediction =', my_pred2
ensure_close(my_pred, my_pred2)

ex.learn() ; ex.learn() ; ex.learn() ; ex.learn()
print '  final partial prediction =', ex.get_updated_prediction()
ensure_close(ex.get_updated_prediction(), my_predict(vw,ex))
print ''
ex.finish()
    
###############################################################################3
exList = []
for i in range(120):    # note: if this is >=129, we hang!!!
    ex = pyvw.example(vw)
    exList.append(ex)

# this is the safe way to delete the examples for VW to reuse:
for ex in exList:
    ex.finish()

exList = [] # this should __del__ the examples, we hope :)
for i in range(120):    # note: if this is >=129, we hang!!!
    ex = pyvw.example(vw)
    exList.append(ex)

for ex in exList:
    ex.finish()

###############################################################################3

for i in range(2):
    ex = pyvw.example(vw, "1 foo| a b")
    ex.learn()
    print 'tag =', ex.get_tag()
    print 'counter =', ex.get_example_counter()
    print 'partial pred =', ex.get_partial_prediction()
    print 'loss =', ex.get_loss()

    print 'label =', pyvw.simple_label(ex)
    ex.finish()


# to be safe, finish explicity (should happen by default anyway)
vw.finish()


###############################################################################3
print '# test some save/load behavior'
vw = pyvw.vw("--quiet -f test.model")
ex = pyvw.example(vw, "1 |x a b |y c")
ex.learn() ; ex.learn() ; ex.learn() ; ex.learn()
before_save = ex.get_updated_prediction()
print 'before saving, prediction =', before_save
ex.finish()
vw.finish()   # this should create the file

# now re-start vw by loading that model
vw = pyvw.vw("--quiet -i test.model")
ex = pyvw.example(vw, "1 |x a b |y c")  # test example
ex.learn()
after_save = ex.get_partial_prediction()
print ' after saving, prediction =', after_save
ex.finish()
ensure_close(before_save, after_save)
vw.finish()   # this should create the file

print 'done!'
