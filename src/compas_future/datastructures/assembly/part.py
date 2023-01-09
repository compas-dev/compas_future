from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import Frame
from compas.geometry import Brep
from compas.geometry import Polyhedron
from compas.datastructures import Mesh
from compas.datastructures import Datastructure
from compas.data import Data


class Feature(Data):
    def apply(self, part):
        raise NotImplementedError

    def restore(self, part):
        raise NotImplementedError

    def accumulate(self, feature):
        """The effect of the given feature shall accumulate with the effect of this one. True is returned if
        the given feature has been consumed by this one.

        False is returned if the feature is not compatible and should be applied independently.

        """
        return False


class GeometricFeature(Feature):

    OPERATIONS = {
        Brep: None,
        Polyhedron: None,
    }

    def __init__(self, name=None):
        super(GeometricFeature, self).__init__(name)
        self._geometry = None
        self._operation = None

    @property
    def data(self):
        return {"geometry": self._geometry}

    @data.setter
    def data(self, value):
        self._geometry = value["geometry"]


class ParametricFeature(Feature):
    def __init__(self, name=None, attribute_name=None, increase_by_value=None):
        super(ParametricFeature, self).__init__(name)
        self._attribute_name = attribute_name
        self._increase_by_value = increase_by_value

    @property
    def data(self):
        return {
            "attribute": self._attribute_name,
            "inc_by_value": self._increase_by_value,
        }

    @data.setter
    def data(self, value):
        self._attribute_name = value["attribute"]
        self._increase_by_value = value["inc_by_value"]


class Part(Datastructure):
    """A data structure for representing assembly parts.

    Parameters
    ----------
    name : str, optional
        The name of the part.
        The name will be stored in :attr:`Part.attributes`.
    frame : :class:`~compas.geometry.Frame`, optional
        The local coordinate system of the part.

    Attributes
    ----------
    attributes : dict[str, Any]
        General data structure attributes that will be included in the data dict and serialization.
    key : int or str
        The identifier of the part in the connectivity graph of the parent assembly.
    frame : :class:`~compas.geometry.Frame`
        The local coordinate system of the part.
    features : list[tuple[:class:`~compas.geometry.Shape`, str]]
        The features added to the base shape of the part geometry.
    geometry : :class:`~compas.geometry.Geometry`, read-only
        A copy of the part's geometry, including applied features, transformed to part.frame.

    """

    def __init__(self, name=None, frame=None, **kwargs):
        super(Part, self).__init__()
        self.attributes = {"name": name or "Part"}
        self.attributes.update(kwargs)
        self.key = None
        self.frame = frame or Frame.worldXY()
        self.features = []

    @property
    def DATASCHEMA(self):
        import schema

        return schema.Schema(
            {
                "attributes": dict,
                "key": int,
                "frame": Frame,
            }
        )

    @property
    def JSONSCHEMANAME(self):
        return "part"

    @property
    def data(self):
        data = {
            "attributes": self.attributes,
            "key": self.key,
            "frame": self.frame,
        }
        return data

    @data.setter
    def data(self, data):
        self.attributes.update(data["attributes"] or {})
        self.key = data["key"]
        self.frame = data["frame"]

    def get_geometry(self, with_features=False):
        """
        Returns a transformed copy of the part's geometry.

        The returned type can be drawn with an Artist.

        Parameters
        ----------
        with_features : bool
            True if geometry should include all the available features.

        Returns
        -------
        :class:`~compas.geometry.Geometry`

        """
        raise NotImplementedError

    def clear_features(self, features_to_clear=None):
        pass

    def add_geometry_feature(self, geometry, operation):
        """
        Add a feature to the shape of the part and the operation through which it should be integrated.

        Parameters
        ----------
        shape : :class:`~compas.assembly.PartGeometry`
            The geometry of the feature.
        operation : Literal['union', 'difference', 'intersection']
            The boolean operation through which the feature should be integrated in the base shape.

        Returns
        -------
        :class: `~compas.datastructures.assembly.part.Feature`
        Returns the instance of the created feature to allow the creator to
        keep track of the features it has created (and "own" them)

        """
        pass

    def add_feature(self, feature):
        """Add a Feature to this Part.

        Parameters
        ----------
        feature : :class:`~compas.assembly.Feature`
            The feature to add
        apply : :bool:
            If True, feature is also applied

        Returns
        -------
        None
        """
        pass

    def to_mesh(self, cls=None):
        """Convert the part geometry to a mesh.

        Parameters
        ----------
        cls : :class:`~compas.datastructures.Mesh`, optional
            The type of mesh to be used for the conversion.

        Returns
        -------
        :class:`~compas.datastructures.Mesh`
            The resulting mesh.

        """
        cls = cls or Mesh
        return cls.from_shape(self.geometry)
