# Here because Python modules require it
# Allows    import thisdir/thefile    from files stored in ./../
#                                     (aka `./../SConstruct` file in our case)
#
# todo: any possible method to remove it?
# maybe doing something wtih sys.path

import sys; sys.dont_write_bytecode=True  # Do not create bytecode __pycache__ folder
