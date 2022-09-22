from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


def mesh_split_edge(mesh, u, v, t=0.5, allow_boundary=False):
    """Split and edge by inserting a vertex along its length.

    Parameters
    ----------
    mesh : :class:`~compas.datastructures.Mesh`
        Instance of a mesh.
    u : int
        The key of the first vertex of the edge.
    v : int
        The key of the second vertex of the edge.
    t : float, optional
        The position of the inserted vertex.
        The value should be between 0.0 and 1.0
    allow_boundary : bool, optional
        If True, also split edges on the boundary.

    Returns
    -------
    int
        The key of the inserted vertex.

    Raises
    ------
    ValueError
        If u and v are not neighbors.

    """
    if t < 0.0:
        raise ValueError("t should be greater than 0.0.")
    if t > 1.0:
        raise ValueError("t should be smaller than 1.0.")

    if t == 0:
        return u
    if t == 1:
        return v

    # check if the split is legal
    # don't split if edge is on boundary
    fkey_uv = mesh.halfedge[u][v]
    fkey_vu = mesh.halfedge[v][u]

    if not allow_boundary:
        if fkey_uv is None or fkey_vu is None:
            return

    # coordinates
    x, y, z = mesh.edge_point(u, v, t)

    # the split vertex
    w = mesh.add_vertex(x=x, y=y, z=z)

    # split half-edge UV
    mesh.halfedge[u][w] = fkey_uv
    mesh.halfedge[w][v] = fkey_uv
    del mesh.halfedge[u][v]

    # update the UV face if it is not the `None` face
    if fkey_uv is not None:
        j = mesh.face[fkey_uv].index(v)
        mesh.face[fkey_uv].insert(j, w)

    # split half-edge VU
    mesh.halfedge[v][w] = fkey_vu
    mesh.halfedge[w][u] = fkey_vu
    del mesh.halfedge[v][u]

    # update the VU face if it is not the `None` face
    if fkey_vu is not None:
        i = mesh.face[fkey_vu].index(u)
        mesh.face[fkey_vu].insert(i, w)

    return w
