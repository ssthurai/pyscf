import numpy as np
from pyscf.pbc.tools import span3

def gen_uniform_grids(cell):
    '''Generate a uniform real-space grid consistent w/ samp thm; see MH (3.19).

    Args:
        cell : instance of :class:`Cell`

    Returns:
        coords : (ngx*ngy*ngz, 3) ndarray
            The real-space grid point coordinates.
        
    '''
    ngs = 2*cell.gs+1
    qv = span3(np.arange(ngs[0]), np.arange(ngs[1]), np.arange(ngs[2]))
    invN = np.diag(1./ngs)
    R = np.dot(np.dot(cell.h, invN), qv)
    coords = R.T.copy() # make C-contiguous with copy() for pyscf
    return coords

class UniformGrids(object):
    '''Uniform Grid class.'''

    def __init__(self, cell):
        self.cell = cell
        self.coords = None
        self.weights = None
        self.stdout = cell.stdout
        self.verbose = cell.verbose

    def setup_grids_(self, cell=None):
        if cell == None: cell = self.cell

        self.coords = gen_uniform_grids(self.cell)
        self.weights = np.ones(self.coords.shape[0]) 
        self.weights *= 1.*cell.vol/self.weights.shape[0]

        return self.coords, self.weights

    def dump_flags(self):
        logger.info(self, 'Uniform grid')

    def kernel(self, cell=None):
        self.dump_flags()
        return self.setup_grids()

