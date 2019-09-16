
import cProfile, pstats, io

def profile(fnc):
    #A decorator that uses cProfile to profile a function
    def inner(*args, **kwargs):

        #create profiler
        pr = cProfile.Profile()

        #profile the function
        pr.enable()
        retval = fnc(*args, **kwargs)
        pr.disable()

        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        return retval
    return inner
