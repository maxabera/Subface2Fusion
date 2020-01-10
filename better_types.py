__all__ = ['Point3D', 'format_point', 'points_eq', 'Matrix', 'ObjectCollectionFromList', 'ObjectCollectionToList', 'ConcatenateObjectCollections']
import adsk.core, adsk.fusion
import math
from numbers import Number

def format_point(point, fmt='{:}'):
  s = '('
  s += fmt.format(point.x)
  s += ', '
  s += fmt.format(point.y)
  if point.z:
    s += ', ' + fmt.format(point.z)
  s += ')'
  return s

def points_eq(p1, p2, epsilon=1e-8):
  if p1 is p2: return True
  if isinstance(p1, adsk.fusion.SketchPoint):
    p1 = p1.geometry
  if isinstance(p2, adsk.fusion.SketchPoint):
    p2 = p2.geometry
  dx = (p1.x - p2.x)**2
  dy = (p1.y - p2.y)**2
  dz = (p1.z - p2.z)**2
  return (dx + dy + dz) <= epsilon**2

def Point3D(x, y, z=0):
  return adsk.core.Point3D.create(x, y, z)


def ObjectCollectionFromList(l):
  oc = adsk.core.ObjectCollection.create()
  for item in l:
    oc.add(item)
  return oc


def ObjectCollectionToList(oc):
  l = []
  for item in oc:
    l.append(item)
  return l


def ConcatenateObjectCollections(l, r):
  for item in r:
    l.add(item)
  return l


class Matrix(object):
  X_AXIS = adsk.core.Vector3D.create(1, 0, 0)
  Y_AXIS = adsk.core.Vector3D.create(0, 1, 0)
  Z_AXIS = adsk.core.Vector3D.create(0, 0, 1)
  ORIGIN = adsk.core.Point3D.create(0, 0, 0)

  def __init__(self, from_matrix=None):
    if from_matrix is None:
      self._m = adsk.core.Matrix3D.create()
    elif isinstance(from_matrix, Matrix):
      self._m = from_matrix._m.copy()
    elif isinstance(from_matrix, adsk.core.Matrix3D):
      self._m = from_matrix.copy()
    else:
      raise 'Invalid transformation matrix type.'

  def as_fusion_matrix3D(self):
    return self._m.copy()

  def copy(self):
    return Matrix(self)

  def identity(self):
    self._m = adsk.core.Matrix3D.create()
    return self

  def translate(self, x_or_point, y=0, z=0):
    if isinstance(x_or_point, Number):
      x = x_or_point
    else:
      x = x_or_point.x
      y = x_or_point.y
      z = x_or_point.z
    m = adsk.core.Matrix3D.create()
    m.translation = adsk.core.Vector3D.create(x, y, z)
    self._m.transformBy(m)
    return self

  def rotate_about_x_axis(self, angle):
    """Rotates about the x-axis."""
    m = adsk.core.Matrix3D.create()
    m.setToRotation(angle, Matrix.X_AXIS, Matrix.ORIGIN)
    self._m.transformBy(m)
    return self

  def rotate_about_y_axis(self, angle):
    """Rotates about the y-axis."""
    m = adsk.core.Matrix3D.create()
    m.setToRotation(angle, Matrix.Y_AXIS, Matrix.ORIGIN)
    self._m.transformBy(m)
    return self

  def rotate_about_z_axis(self, angle):
    """Rotates about the z-axis."""
    m = adsk.core.Matrix3D.create()
    m.setToRotation(angle, Matrix.Z_AXIS, Matrix.ORIGIN)
    self._m.transformBy(m)
    return self

  def scale(self, x=1, y=1, z=1):
    a = [x, 0, 0, 0,
         0, y, 0, 0,
         0, 0, z, 0,
         0, 0, 0, 1]

    m = adsk.core.Matrix3D.create()
    m.setWithArray(a)
    self.multiply(m)
    return self

  def reflect_about_yz(self):
    """Reflects through the X axis about the YZ plane."""
    return self.scale(-1, 1, 1)

  def reflect_about_xz(self):
    """Reflects through the Y axis about the XZ plane."""
    return self.scale(1, -1, 1)

  def reflect_about_xy(self):
    """Reflects through the Z axis about the XY plane."""
    return self.scale(1, 1, -1)

  def multiply(self, other):
    self._m.transformBy(other)
    return self

  def purify(self):
    a = self._m.asArray()
    b = []
    for i in range(16):
      if abs(a[i]) < 1e-15:
        b.append(0)
      elif abs(abs(a[i]) - 1) < 1e-15:
        if a[i] < 0:
          b.append(-1)
        else:
          b.append(1)
      else:
        b.append(a[i])
    self._m.setWithArray(b)
    return self

  def transform(self, x_or_points, y=0, z=0):
    """Transforms a list of points, a single point, or a literal x,y,z
    and returns a new list of, or single, transformed point(s).

    Args:
      x_or_points: May be a list of points, a single point, or a number representing 'x'.
      y: y cord
      z: z cord
    """
    if isinstance(x_or_points, list):
      new_points = []
      for p in x_or_points:
        b = p.copy()
        b.transformBy(self._m)
        new_points.append(b)
      return new_points

    if isinstance(x_or_points, Number):
      b = Point3D(x_or_points, y, z)
    else:
      assert isinstance(x_or_points, adsk.core.Point3D) or isinstance(x_or_points, adsk.core.Vector3D)
      b = x_or_points.copy()

    b.transformBy(self._m)
    return b

  def vectorTransform():
    ui = None
    try:
      app = adsk.core.Application.get()
      ui = app.userInterface

      vec = adsk.core.Vector3D.create(1, 0, 0)
      mat = adsk.core.Matrix3D.create()
      mat.setToRotation(math.pi / 2, adsk.core.Vector3D.create(0, 0, 1), adsk.core.Point3D.create(0, 0, 0))
      ui.messageBox(str(vec.asArray()))
      vec.transformBy(mat)
      ui.messageBox(str(vec.asArray()))
    except:
      if ui:
        ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))