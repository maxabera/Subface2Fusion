import params
import vector
import math
import adsk

# from  subface/publisher/f360/beams.py

beams_column_names = [
    params.NODE_IDX0,
    params.NODE_IDX1,
    params.HEIDX0,
    params.FIIDX0,
    params.FIIDX1,
    params.BEAM_START_X,
    params.BEAM_START_Y,
    params.BEAM_START_Z,
    params.BEAM_END_X,
    params.BEAM_END_Y,
    params.BEAM_END_Z,
    params.ANGLE
]

newComp = None

class Beam:

    default_inner_diameter = 8
    default_outer_diameter = 10
    default_coordinates = [[0, 0, 0], [10, 10, 10]]
    
    def __init__(self):
        self.nodidx0 = -1
        self.nodidx1 = -1

        self.heidx0 = -1    # left  vidx0 -> vidx1
        self.heidx1 = -1    # right vidx1 -> vidx0

        self.fiidx0 = -1    # finger0 index
        self.fiidx1 = -1    # finger1 index
        self.fii_len0 = 0   # finger0 length
        self.fii_len1 = 0   # finger1 length

        self.fiisqn0 = -1   # finger0 sequence number
        self.fiisqn1 = -1   # finger1 sequence number

        self.coordinates = Beam.default_coordinates  # [[x0,y0,z0], [x1,y1,z1]]
        self.start = [0,0,0]
        self.end = [10, 10, 10]
        self.offset0 = 0  #
        self.offset1 = 0  #
        self.x_base = [1, 1, 1]
        self.angle = 0 # angle of connecting faces

        self._inner_d = Beam.default_inner_diameter
        self._outer_d = Beam.default_outer_diameter
        self.is_ignored = False

    #properties
    
    @property
    def inner_diameter(self):
        return self._inner_d
    
    @inner_diameter.setter
    def inner_diameter(self, value):
        self._inner_d = value
    
    @property
    def outer_diameter(self):
        return self._outer_d
    
    @outer_diameter.setter
    def outer_diameter(self, value):
        self._outer_d = value
        
    @property
    def start_position(self):
        return self.coordinates[0]
    
    @start_position.setter
    def start_position(self, value):
        self.coordinates[0] = value
    
    @property
    def end_position(self):
        return self.coordinates[1]
    
    @end_position.setter
    def end_position(self, value):
        self.coordinates[1] = value

    @property
    def name(self):
        a_name = "BEAM{:03d}F{:02d}T{:03d}F{:02d}".format(self.nodidx0, self.fiisqn0, self.nodidx1, self.fiisqn1)
        return a_name


    @property
    def length(self):        
        ax, ay, az = self.coordinates[0]
        bx, by, bz = self.coordinates[1]
        dd = (bx-ax)*(bx-ax) + (by-ay)*(by-ay) + (bz-az)*(bz-az)
        return math.sqrt(dd)

    def parse_json(self, json_beam):
            
        beam_start = self.get_param(json_beam, params.BEAM_START, [0,0,0])
        beam_end = self.get_param(json_beam, params.BEAM_END, [0,0,10])
        coords = [beam_start, beam_end]
        self.coordinates = coords
        self.nodidx0 = self.get_param(json_beam, params.NODE_IDX0, -1)
        self.nodidx1 = self.get_param(json_beam, params.NODE_IDX1, -1)
        
        self.heidx0 = self.get_param(json_beam, params.HEIDX0, -1)
        self.heidx1 = self.get_param(json_beam, params.HEIDX1, -1)
        
        self.fiidx0 = self.get_param(json_beam, params.FIIDX0, -1)
        self.fiidx1 = self.get_param(json_beam, params.FIIDX1, -1)
        self.fii_len0 = self.get_param(json_beam, params.FIILEN0, -1)
        self.fii_len1 = self.get_param(json_beam, params.FIILEN1, -1)  # finger1 length
        self.fiisqn0 = self.get_param(json_beam, params.FIISQN0, -1)   # finger0 sequence number
        self.fiisqn1 = self.get_param(json_beam, params.FIISQN1, -1)   # finger1 sequence number
        self.x_base = self.get_param(json_beam, params.XBASE, -1)
        self.angle = self.get_param(json_beam, params.FACE_ANGLE, -1)  # angle of connecting faces

        return True


    def get_param(self, json_data, param_name, default):
        
        value = None
        if not param_name in json_data:
            print("parameter {} not found".format(param_name))
            value = default
        else:
            value = json_data[param_name]
            
        return value
        

    def buildObject(self, newComp):

        # Create a new sketch.
        sketches = newComp.sketches
        xyPlane = newComp.xYConstructionPlane
        sketch0 = sketches.add(xyPlane)
        
        circles = sketch0.sketchCurves.sketchCircles
        
        p0 = adsk.core.Point3D.create(0, 0, 0)
    
        # create beam profile
        if self._outer_d > 0:
            circles.addByCenterRadius(p0, self._outer_d/2.0)  # outer circle
        if self._inner_d > 0:
            circles.addByCenterRadius(p0, self._inner_d/2.0)  # inner circle

        if self.length != 0:        
            distance = adsk.core.ValueInput.createByReal(self.length)           
            prof = sketch0.profiles.item(0)              
            # mm150 = adsk.core.ValueInput.createByString("150 mm")
            # mm0 = adsk.core.ValueInput.createByString("0 mm")        
            extrudes = newComp.features.extrudeFeatures        
            extrudeInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
            distanceDefinition = adsk.fusion.DistanceExtentDefinition.create(distance)
            extrudeInput.setOneSideExtent(distanceDefinition, adsk.fusion.ExtentDirections.PositiveExtentDirection)
            obj = extrudes.add(extrudeInput)
            if obj.bodies.count > 0:
                body = obj.bodies.item(0)
                body.name = "Konecne"
            obj.name = "myTube"
            obj.partNumber = "xyss75478"
            
            # Create a collection of entities for move
            bodies = adsk.core.ObjectCollection.create()
            bodies.add(obj.bodies.item(0))    
    
            # Create a transform to do move
            move_vector = adsk.core.Vector3D.create(self.start_position[0],
                                                    self.start_position[1],
                                                    self.start_position[2])
            
            vec = vector.create(self.start_position, self.end_position)
            vec_length = vector.magnitude(vec)
            
            beam_vector = adsk.core.Vector3D.create(vec[0], vec[1], vec[2])
            start_vector = adsk.core.Vector3D.create(0, 0, 1)
            beam_vector.normalize()
                    
            # radial distance
            transform = adsk.core.Matrix3D.create()
            transform.setToRotateTo(start_vector, beam_vector)
            moveFeats = newComp.features.moveFeatures
            moveFeatureInput = moveFeats.createInput(bodies, transform)
            moveFeats.add(moveFeatureInput)
                    
            if move_vector.length != 0:
                transform = adsk.core.Matrix3D.create()
                transform.translation = move_vector
                moveFeats = newComp.features.moveFeatures
                moveFeatureInput = moveFeats.createInput(bodies, transform)
                moveFeats.add(moveFeatureInput)
