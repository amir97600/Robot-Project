import numpy as np
from copy import deepcopy


def Eij(i, j, n, m):
    """
    >>> Eij(1, 2, 3, 4)
    array([[0., 0., 0., 0.],
           [0., 0., 1., 0.],
           [0., 0., 0., 0.]])
    """
    return np.array([
        [
            1.0 if kk == i and ll == j else 0
            for ll in range(m)
        ]
        for kk in range(n)
    ])


def symEij(i, j, n):
    """
    >>> symEij(1, 2, 3)
    array([[0., 0., 0.],
           [0., 0., 1.],
           [0., 1., 0.]])
    """
    if i == j:
        return Eij(i, j, n, n)
    return Eij(i, j, n, n) + Eij(j, i, n, n)


def to_1D(T, mask):
    """
    >>> A = np.array([[1,2],[3,4],[5,6]])
    >>> mask = np.array([[1,0],[1,0],[1,1]])
    >>> to_1D(A, mask).T
    array([[1, 3, 5, 6]])

    >>> A = np.array([[1,2],[3,4],[5,6]])
    >>> mask = np.array([[1,0],[0,1],[0,1]])
    >>> to_1D(A, mask).T
    array([[1, 4, 6]])
    """
    assert(T.shape == mask.shape)
    T = T.reshape(-1)
    mask = mask.reshape(-1)
    res = []
    for i in range(mask.size):
        if mask[i] > 0:
            res.append(T[i])
    res = np.array(res)
    return res.reshape((-1, 1))


def solve_linear_equation(
    A, fct,
    symetric_n=None, rectangular_n=None,
    symetric_mask=None, rectangular_mask=None,
    output_mask=None
):
    """
    A = fct([S1, S2, ...], [M1, M2, ...])

    S1, S2, ... are symetric of size in symetric_n
    M1, M2, ... are rectangular of geometry (x,y sizes) in rectangular_n

    >>> def fct(L1, L2):
    ...     S1, S2, = L1
    ...     M1, M2, = L2
    ...     return (
    ...         np.array([
    ...             [-1,  4],
    ...             [-3,  6],
    ...             [ 1,  1],
    ...             [ 0, -1],
    ...             [ 1,  2],
    ...             [ 4,  1]
    ...         ]) @ S1 @ np.array([
    ...             [-1, 4, 7,  1],
    ...             [-3, 6, 9, -2]
    ...         ])
    ...         +
    ...         np.array([
    ...             [-2,  1,  1],
    ...             [-5,  2,  3],
    ...             [ 1, -2,  0],
    ...             [ 1,  0,  2],
    ...             [ 2,  1,  2],
    ...             [-3,  2, -1]
    ...         ]) @ S2 @ np.array([
    ...             [ -2, 3, 1,  0],
    ...             [ -2, 3, 1, -1],
    ...             [  2, 1, 4,  2]
    ...         ])
    ...         +
    ...         np.array([
    ...             [-1,  2,  3],
    ...             [ 1,  4,  1],
    ...             [ 4,  1, -4],
    ...             [-2, -1,  0],
    ...             [ 0,  3,  1],
    ...             [ 1,  0,  2]
    ...         ]) @ M1 @ np.array([
    ...             [0, 4, 1,  3],
    ...             [-1, 2, 3, 0]
    ...         ])
    ...         +
    ...         np.array([
    ...             [-2,  2,  1],
    ...             [ 4,  2,  1],
    ...             [ 0,  0,  5],
    ...             [ 1,  1,  2],
    ...             [ 1, -3,  1],
    ...             [ 0,  1,  3]
    ...         ]) @ M2 @ np.array([
    ...             [1, 0, -1,  2],
    ...         ])
    ...      )
    >>> S1 = np.array([[2,6],[6,3]])
    >>> S2 = np.array([
    ...     [5,  1, 0],
    ...     [1, -1, 1],
    ...     [0,  1, 1]
    ... ])
    >>> M1 = np.array([
    ...     [-1,  1],
    ...     [ 3, -2],
    ...     [ 2,  5],
    ... ])
    >>> M2 = np.array([
    ...     [  5],
    ...     [ -2],
    ...     [  1],
    ... ])
    >>> A = fct([S1, S2], [M1, M2])
    >>> res_S, res_M, det = solve_linear_equation(
    ...     A, fct, [2, 3], [(3, 2), (3,1)]
    ... )
    >>> np.abs(det) > 10**-3
    True
    >>> np.linalg.norm(A - fct(res_S, res_M)) < 10**-8
    True
    >>> np.linalg.norm(A - fct(res_S, res_M)) < 10**-8
    True

    >>> output_mask = np.array([
    ...     [ 1, 0, 1, 1],
    ...     [ 1, 1, 1, 1],
    ...     [ 1, 1, 0, 1],
    ...     [ 1, 0, 0, 1],
    ...     [ 1, 1, 1, 0],
    ...     [ 1, 1, 1, 0]
    ... ])
    >>> res_S, res_M, det = solve_linear_equation(
    ...     A, fct, [2, 3], [(3, 2), (3,1)], output_mask=output_mask
    ... )
    >>> np.abs(det) > 10**-3
    True
    >>> np.linalg.norm(A - fct(res_S, res_M)) < 10**-8
    True

    >>> output_mask = np.array([
    ...     [ 1, 0, 1, 1],
    ...     [ 0, 0, 1, 1],
    ...     [ 1, 1, 0, 1],
    ...     [ 1, 0, 0, 1],
    ...     [ 1, 1, 1, 0],
    ...     [ 0, 1, 1, 0]
    ... ])
    >>> res_S, res_M, det = solve_linear_equation(
    ...     A, fct, [2, 3], [(3, 2), (3,1)], output_mask=output_mask
    ... )
    >>> np.abs(det) < 10**-3
    True
    >>> np.linalg.norm(A - fct(res_S, res_M)) < 10**-8
    False

    >>> S1 = np.array([[2,6],[6,0]])
    >>> S1_mask = np.array([[1,1],[1,0]])
    >>> S2 = np.array([
    ...     [5,  0, 0],
    ...     [0, -1, 1],
    ...     [0,  1, 0]
    ... ])
    >>> S2_mask = np.array([
    ...     [1,  0, 0],
    ...     [0,  1, 1],
    ...     [0,  1, 0]
    ... ])
    >>> M1 = np.array([
    ...     [ 0,  1],
    ...     [ 0,  0],
    ...     [ 2,  0],
    ... ])
    >>> M1_mask = np.array([
    ...     [ 0,  1],
    ...     [ 1,  0],
    ...     [ 1,  0],
    ... ])
    >>> M2 = np.array([
    ...     [  0],
    ...     [ -2],
    ...     [  1],
    ... ])
    >>> M2_mask = np.array([
    ...     [  0],
    ...     [  1],
    ...     [  1],
    ... ])
    >>> A = fct([S1, S2], [M1, M2])
    >>> res_S, res_M, det = solve_linear_equation(
    ...     A, fct,
    ...     symetric_mask = [S1_mask, S2_mask],
    ...     rectangular_mask = [M1_mask, M2_mask]
    ... )
    >>> np.abs(det) > 10**-3
    True
    >>> np.linalg.norm(A - fct(res_S, res_M)) < 10**-8
    True
    """
    if symetric_n is None:
        symetric_n = [S.shape[0] for S in symetric_mask]
    if rectangular_n is None:
        rectangular_n = [M.shape for M in rectangular_mask]

    if symetric_mask is None:
        symetric_mask = [
            np.full((n, n), 1)
            for n in symetric_n
        ]
    if rectangular_mask is None:
        rectangular_mask = [
            np.full((m, n), 1)
            for m, n in rectangular_n
        ]

    if output_mask is None:
        output_mask = np.full(A.shape, 1)

    zero_S = [np.zeros((n, n)) for n in symetric_n]
    zero_M = [np.zeros((m, n)) for m, n in rectangular_n]

    image_fct_S = []
    nb_parameters_S = [0]
    for k in range(len(symetric_n)):
        n = symetric_n[k]
        images = []
        for i, j in zip(*np.triu_indices(n)):
            if symetric_mask[k][i, j] > 0:
                e_S = deepcopy(zero_S)
                e_M = deepcopy(zero_M)
                e_S[k] = symEij(i, j, n)
                images.append(to_1D(fct(e_S, e_M), output_mask))
        if len(images) != 0:
            image_fct_S.append(np.hstack(images))
        nb_parameters_S.append(nb_parameters_S[-1] + len(images))

    image_fct_M = []
    nb_parameters_M = [0]
    for k in range(len(rectangular_n)):
        m, n = rectangular_n[k]
        images = []
        for i in range(m):
            for j in range(n):
                if rectangular_mask[k][i, j] > 0:
                    e_S = deepcopy(zero_S)
                    e_M = deepcopy(zero_M)
                    e_M[k] = Eij(i, j, m, n)
                    images.append(to_1D(fct(e_S, e_M), output_mask))
        if len(images) != 0:
            image_fct_M.append(np.hstack(images))
        nb_parameters_M.append(nb_parameters_M[-1] + len(images))

    F = np.hstack(image_fct_S + image_fct_M)

    det = np.linalg.det(F.T @ F)

    # sol = np.linalg.inv(F.T @ F) @ F.T @ A.reshape((-1,1))
    reshaped_output = to_1D(A, output_mask)
    sol = np.linalg.pinv(F) @ reshaped_output
    sol = sol.reshape(-1)

    parameter_S, parameter_M = np.split(sol, [nb_parameters_S[-1]])
    parameter_S = np.split(parameter_S, nb_parameters_S)[1:-1]
    parameter_M = np.split(parameter_M, nb_parameters_M)[1:-1]

    sol_S = []
    for k in range(len(symetric_n)):
        n = symetric_n[k]
        S = np.zeros((n, n))
        cpt = 0
        for i, j in zip(*np.triu_indices(n)):
            if(symetric_mask[k][i, j] > 0):
                S[i, j] = parameter_S[k][cpt]
                S[j, i] = parameter_S[k][cpt]
                cpt += 1
        sol_S.append(S)

    sol_M = []
    for k in range(len(rectangular_n)):
        m, n = rectangular_n[k]
        M = np.zeros((m, n))
        cpt = 0
        for i in range(m):
            for j in range(n):
                if rectangular_mask[k][i, j] > 0:
                    M[i, j] = parameter_M[k][cpt]
                    cpt += 1
        sol_M.append(M)

    return [sol_S, sol_M, det]


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    def fct(L1, L2):
        S1, S2, = L1
        M1, M2, = L2
        return (
            np.array([
                [-1,  4],
                [-3,  6],
                [ 1,  1],
                [ 0, -1],
                [ 1,  2],
                [ 4,  1]
            ]) @ S1 @ np.array([
                [-1, 4, 7,  1],
                [-3, 6, 9, -2]
            ])
            +
            np.array([
                [-2,  1,  1],
                [-5,  2,  3],
                [ 1, -2,  0],
                [ 1,  0,  2],
                [ 2,  1,  2],
                [-3,  2, -1]
            ]) @ S2 @ np.array([
                [ -2, 3, 1,  0],
                [ -2, 3, 1, -1],
                [  2, 1, 4,  2]
            ])
            +
            np.array([
                [-1,  2,  3],
                [ 1,  4,  1],
                [ 4,  1, -4],
                [-2, -1,  0],
                [ 0,  3,  1],
                [ 1,  0,  2]
            ]) @ M1 @ np.array([
                [0, 4, 1,  3],
                [-1, 2, 3, 0]
            ])
            +
            np.array([
                [-2,  2,  1],
                [ 4,  2,  1],
                [ 0,  0,  5],
                [ 1,  1,  2],
                [ 1, -3,  1],
                [ 0,  1,  3]
            ]) @ M2 @ np.array([
                [1, 0, -1,  2],
            ])
         )
    S1 = np.array([[2, 6],[6, 3]])
    S2 = np.array([
        [5,  1, 0],
        [1, -1, 1],
        [0,  1, 1]
    ])
    M1 = np.array([
        [-1,  1],
        [ 3, -2],
        [ 2,  5],
    ])
    M2 = np.array([
        [ 5],
        [-2],
        [ 1],
    ])

    A = fct([S1, S2], [M1, M2])
    output_mask = np.array([
        [1, 0, 1, 1],
        [1, 0, 1, 1],
        [1, 1, 0, 1],
        [1, 0, 0, 1],
        [1, 1, 1, 0],
        [1, 1, 1, 0]
    ])
    res_S, res_M, det = solve_linear_equation(
        A, fct, [2, 3], [(3, 2), (3, 1)], output_mask=output_mask
    )
    det > 10**-3
    np.linalg.norm(A - fct(res_S, res_M)) < 10**-8
