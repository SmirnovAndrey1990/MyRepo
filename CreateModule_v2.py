"""
Example Script for MacroPlacements
"""
import math as m
import hashlib as hashlib

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_Precast as AllplanPrecast
import NemAll_Python_AllplanSettings as AllplanSettings

from StdReinfShapeBuilder.RotationAngles import RotationAngles

from PythonPart import View2D3D, PythonPart

from HandleDirection import HandleDirection
from HandleProperties import HandleProperties

def check_allplan_version(build_ele, version):
    """
    Check the current Allplan version

    Args:
        build_ele: the building element.
        version:   the current Allplan version

    Returns:
        True/False if version is supported by this script
    """

    # Delete unused arguments
    del build_ele
    del version

    # Support all versions
    return True


def create_element(build_ele, doc):
    module = Create_Module(build_ele)
    module.create_wall()
    model_ele_list = module.model_ele_list
    handle_list = module.handle_list
    return (model_ele_list, handle_list)


def move_handle(build_ele, handle_prop, input_pnt, doc):
    build_ele.change_property(handle_prop, input_pnt)  
    return create_element(build_ele, doc)

class Create_Module(): 
    def __init__(self, build_ele):
        self.build_ele = build_ele
        self.model_ele_list = []
        self.fixture_elements = []
        self.handle_list = []
        self.library_ele_list = []
        
        self.slab_thick = build_ele.SlabThick.value
        self.module_type = build_ele.ModuleType.value
        self.pylon_thick_eq_wall_thick = build_ele.PylonThickEqWallThick.value 
        self.create_filling = build_ele.CreateFilling.value
        self.create_handle = build_ele.CreateHandle.value
        self.python_part = build_ele.CreatePythonPart.value
        self.wall_offset = [None, None]
        self.orient_params = [None, None, None, None]

        #-----------------------------------------------------------FIRST WALL----------------------------------------------------------------------
        self.create_wall1 = build_ele.CreateWall1.value
        self.wall1 = [build_ele.ModuleLength.value, build_ele.WallThick.value, "ModuleLength", None, None]
        self.left_end1 = [build_ele.LeftEnd1.value, build_ele.LeftEndLength1.value, build_ele.LeftPylonLength1.value]
        self.right_end1 = [build_ele.RightEnd1.value, build_ele.RightEndLength1.value, build_ele.RightPylonLength1.value]
        self.pylon_num1 = build_ele.PylonNum1.value 
        self.orient_params1 = [HandleDirection.x_dir, 0, 0, 0]
        
        self.fir_cent_pylon1 = [build_ele.FirstCentPylonLength1.value, build_ele.FirstCentPylonThick1.value, build_ele.FirstCentPylonPosit1.value, "FirstCentPylonPosit1"]
        self.sec_cent_pylon1 = [build_ele.SecondCentPylonLength1.value, build_ele.SecondCentPylonThick1.value, build_ele.SecondCentPylonPosit1.value, "SecondCentPylonPosit1"]
        self.thi_cent_pylon1 = [build_ele.ThirdCentPylonLength1.value, build_ele.ThirdCentPylonThick1.value, build_ele.ThirdCentPylonPosit1.value, "ThirdCentPylonPosit1"]

        self.fir_sect_wall1 = [build_ele.FirstSectWall1.value, build_ele.FirstSectWallLength1.value, build_ele.FirstSectWallPosit1.value, "FirstSectWallPosit1"]
        self.sec_sect_wall1 = [build_ele.SecondSectWall1.value, build_ele.SecondSectWallLength1.value, build_ele.SecondSectWallPosit1.value, "SecondSectWallPosit1"]
        self.thi_sect_wall1 = [build_ele.ThirdSectWall1.value, build_ele.ThirdSectWallLength1.value, build_ele.ThirdSectWallPosit1.value, "ThirdSectWallPosit1"]
        self.fou_sect_wall1 = [build_ele.FourthSectWall1.value, build_ele.FourthSectWallLength1.value, build_ele.FourthSectWallPosit1.value, "FourthSectWallPosit11"]
        self.fif_sect_wall1 = [build_ele.FifthSectWall1.value, build_ele.FifthSectWallLength1.value, build_ele.FifthSectWallPosit1.value, "FifthSectWallPosit1"]
        self.six_sect_wall1 = [build_ele.SixthSectWall1.value, build_ele.SixthSectWallLength1.value, build_ele.SixthSectWallPosit1.value, "SixthSectWallPosit1"]
        self.sev_sect_wall1 = [build_ele.SeventhSectWall1.value, build_ele.SeventhSectWallLength1.value, build_ele.SeventhSectWallPosit1.value, "SeventhSectWallPosit1"]
        self.eig_sect_wall1 = [build_ele.EighthSectWall1.value, build_ele.EighthSectWallLength1.value, build_ele.EighthSectWallPosit1.value, "EighthSectWallPosit1"]
       
        self.fir_open1 = [build_ele.FirstOpening1.value, build_ele.FirstOpeningWidth1.value, build_ele.FirstOpeningHeight1.value,
                          build_ele.FirstOpeningXPosit1.value, build_ele.FirstOpeningZPosit1.value, "FirstOpeningXPosit1", "FirstOpeningWidth1"]
        self.sec_open1 = [build_ele.SecondOpening1.value, build_ele.SecondOpeningWidth1.value, build_ele.SecondOpeningHeight1.value,
                          build_ele.SecondOpeningXPosit1.value, build_ele.SecondOpeningZPosit1.value, "SecondOpeningXPosit1", "SecondOpeningWidth1"]
        self.thi_open1 = [build_ele.ThirdOpening1.value, build_ele.ThirdOpeningWidth1.value, build_ele.ThirdOpeningHeight1.value,
                          build_ele.ThirdOpeningXPosit1.value, build_ele.ThirdOpeningZPosit1.value, "ThirdOpeningXPosit1", "ThirdOpeningWidth1"]
        self.fou_open1 = [build_ele.FourthOpening1.value, build_ele.FourthOpeningWidth1.value, build_ele.FourthOpeningHeight1.value,
                          build_ele.FourthOpeningXPosit1.value, build_ele.FourthOpeningZPosit1.value, "FourthOpeningXPosit1", "FourthOpeningWidth1"]
        self.fif_open1 = [build_ele.FifthOpening1.value, build_ele.FifthOpeningWidth1.value, build_ele.FifthOpeningHeight1.value,
                          build_ele.FifthOpeningXPosit1.value, build_ele.FifthOpeningZPosit1.value, "FifthOpeningXPosit1", "FifthOpeningWidth1"]
        self.six_open1 = [build_ele.SixthOpening1.value, build_ele.SixthOpeningWidth1.value, build_ele.SixthOpeningHeight1.value,
                          build_ele.SixthOpeningXPosit1.value, build_ele.SixthOpeningZPosit1.value, "SixthOpeningXPosit1", "SixthOpeningWidth1"]      
        self.sev_open1 = [build_ele.SeventhOpening1.value, build_ele.SeventhOpeningWidth1.value, build_ele.SeventhOpeningHeight1.value,
                          build_ele.SeventhOpeningXPosit1.value, build_ele.SeventhOpeningZPosit1.value, "SeventhOpeningXPosit1", "SeventhOpeningWidth1"]
        self.eig_open1 = [build_ele.EighthOpening1.value, build_ele.EighthOpeningWidth1.value, build_ele.EighthOpeningHeight1.value,
                          build_ele.EighthOpeningXPosit1.value, build_ele.EighthOpeningZPosit1.value, "EighthOpeningXPosit1", "EighthOpeningWidth1"]
        self.nin_open1 = [build_ele.NinthOpening1.value, build_ele.NinthOpeningWidth1.value, build_ele.NinthOpeningHeight1.value,
                          build_ele.NinthOpeningXPosit1.value, build_ele.NinthOpeningZPosit1.value, "NinthOpeningXPosit1", "NinthOpeningWidth1"]
        self.ten_open1 = [build_ele.TenthOpening1.value, build_ele.TenthOpeningWidth1.value, build_ele.TenthOpeningHeight1.value,
                          build_ele.TenthOpeningXPosit1.value, build_ele.TenthOpeningZPosit1.value, "TenthOpeningXPosit1", "TenthOpeningWidth1"]
        self.ele_open1 = [build_ele.EleventhOpening1.value, build_ele.EleventhOpeningWidth1.value, build_ele.EleventhOpeningHeight1.value,
                          build_ele.EleventhOpeningXPosit1.value, build_ele.EleventhOpeningZPosit1.value, "EleventhOpeningXPosit1", "EleventhOpeningWidth1"]
        self.twe_open1 = [build_ele.TwelfthOpening1.value, build_ele.TwelfthOpeningWidth1.value, build_ele.TwelfthOpeningHeight1.value,
                          build_ele.TwelfthOpeningXPosit1.value, build_ele.TwelfthOpeningZPosit1.value, "TwelfthOpeningXPosit1", "TwelfthOpeningWidth1"]

        self.fir_door1 = [build_ele.FirstDoor1.value, build_ele.FirstDoorWidth1.value, build_ele.FirstDoorHeight1.value,
                          build_ele.FirstDoorXPosit1.value, build_ele.FirstDoorZPosit1.value, "FirstDoorXPosit1", "FirstDoorWidth1"]
        self.sec_door1 = [build_ele.SecondDoor1.value, build_ele.SecondDoorWidth1.value, build_ele.SecondDoorHeight1.value,
                          build_ele.SecondDoorXPosit1.value, build_ele.SecondDoorZPosit1.value, "SecondDoorXPosit1", "SecondDoorWidth1"]
        self.thi_door1 = [build_ele.ThirdDoor1.value, build_ele.ThirdDoorWidth1.value, build_ele.ThirdDoorHeight1.value,
                          build_ele.ThirdDoorXPosit1.value, build_ele.ThirdDoorZPosit1.value, "ThirdDoorXPosit1", "ThirdDoorWidth1"]
        self.fou_door1 = [build_ele.FourthDoor1.value, build_ele.FourthDoorWidth1.value, build_ele.FourthDoorHeight1.value,
                          build_ele.FourthDoorXPosit1.value, build_ele.FourthDoorZPosit1.value, "FourthDoorXPosit1", "FourthDoorWidth1"]
        self.fif_door1 = [build_ele.FifthDoor1.value, build_ele.FifthDoorWidth1.value, build_ele.FifthDoorHeight1.value,
                          build_ele.FifthDoorXPosit1.value, build_ele.FifthDoorZPosit1.value, "FifthDoorXPosit1", "FifthDoorWidth1"]
        self.six_door1 = [build_ele.SixthDoor1.value, build_ele.SixthDoorWidth1.value, build_ele.SixthDoorHeight1.value,
                          build_ele.SixthDoorXPosit1.value, build_ele.SixthDoorZPosit1.value, "SixthDoorXPosit1", "SixthDoorWidth1"]      
        self.sev_door1 = [build_ele.SeventhDoor1.value, build_ele.SeventhDoorWidth1.value, build_ele.SeventhDoorHeight1.value,
                          build_ele.SeventhDoorXPosit1.value, build_ele.SeventhDoorZPosit1.value, "SeventhDoorXPosit1", "SeventhDoorWidth1"]
        self.eig_door1 = [build_ele.EighthDoor1.value, build_ele.EighthDoorWidth1.value, build_ele.EighthDoorHeight1.value,
                          build_ele.EighthDoorXPosit1.value, build_ele.EighthDoorZPosit1.value, "EighthDoorXPosit1", "EighthDoorWidth1"]
        self.nin_door1 = [build_ele.NinthDoor1.value, build_ele.NinthDoorWidth1.value, build_ele.NinthDoorHeight1.value,
                          build_ele.NinthDoorXPosit1.value, build_ele.NinthDoorZPosit1.value, "NinthDoorXPosit1", "NinthDoorWidth1"]
        self.ten_door1 = [build_ele.TenthDoor1.value, build_ele.TenthDoorWidth1.value, build_ele.TenthDoorHeight1.value,
                          build_ele.TenthDoorXPosit1.value, build_ele.TenthDoorZPosit1.value, "TenthDoorXPosit1", "TenthDoorWidth1"]
        self.ele_door1 = [build_ele.EleventhDoor1.value, build_ele.EleventhDoorWidth1.value, build_ele.EleventhDoorHeight1.value,
                          build_ele.EleventhDoorXPosit1.value, build_ele.EleventhDoorZPosit1.value, "EleventhDoorXPosit1", "EleventhDoorWidth1"]
        self.twe_door1 = [build_ele.TwelfthDoor1.value, build_ele.TwelfthDoorWidth1.value, build_ele.TwelfthDoorHeight1.value,
                          build_ele.TwelfthDoorXPosit1.value, build_ele.TwelfthDoorZPosit1.value, "TwelfthDoorXPosit1", "TwelfthDoorWidth1"]

        self.open1 = [self.fir_open1, self.sec_open1, self.thi_open1, self.fou_open1, self.fif_open1, self.six_open1, 
                     self.sev_open1, self.eig_open1, self.nin_open1, self.ten_open1, self.ele_open1, self.twe_open1]
        self.door1 = [self.fir_door1, self.sec_door1, self.thi_door1, self.fou_door1, self.fif_door1, self.six_door1, 
                     self.sev_door1, self.eig_door1, self.nin_door1, self.ten_door1, self.ele_door1, self.twe_door1]

        for open, door in zip(self.open1, self.door1):
            if door[0]:
                for idx in range(len(door)):
                    open[idx] = door[idx]

        self.insul1 = [build_ele.CreateInsulation1.value, build_ele.InsulWidth.value, build_ele.InsulHeight.value, 
                       build_ele.InsulThick.value, build_ele.InsulMinWidth.value]
        self.insul_type1 = build_ele.ThrLayPanel1.value

        self.hor_rib_thick1, self.ver_rib_thick1  = build_ele.HorRibThick1.value, build_ele.VerRibThick1.value
        self.open_hor_rib_thick1, self.open_ver_rib_thick1 = build_ele.OpenHorRibThick1.value, build_ele.OpenVerRibThick1.value

        #-----------------------------------------------------------SECOND WALL---------------------------------------------------------------------
        self.create_wall2 = build_ele.CreateWall2.value
        self.wall2 = [build_ele.ModuleWidth.value, build_ele.WallThick.value,"ModuleWidth", None, None]
        self.left_end2 = [build_ele.LeftEnd2.value, build_ele.LeftEndLength2.value, build_ele.LeftPylonLength2.value]
        self.right_end2 = [build_ele.RightEnd2.value, build_ele.RightEndLength2.value, build_ele.RightPylonLength2.value]
        self.pylon_num2 = build_ele.PylonNum2.value 
        self.orient_params2 = [HandleDirection.y_dir, self.wall1[0], 0, 90]
        
        self.fir_cent_pylon2 = [build_ele.FirstCentPylonLength2.value, build_ele.FirstCentPylonThick2.value, build_ele.FirstCentPylonPosit2.value, "FirstCentPylonPosit2"]
        self.sec_cent_pylon2 = [build_ele.SecondCentPylonLength2.value, build_ele.SecondCentPylonThick2.value, build_ele.SecondCentPylonPosit2.value, "SecondCentPylonPosit2"]
        self.thi_cent_pylon2 = [build_ele.ThirdCentPylonLength2.value, build_ele.ThirdCentPylonThick2.value, build_ele.ThirdCentPylonPosit2.value, "ThirdCentPylonPosit2"]

        self.fir_sect_wall2 = [build_ele.FirstSectWall2.value, build_ele.FirstSectWallLength2.value, build_ele.FirstSectWallPosit2.value, "FirstSectWallPosit2"]
        self.sec_sect_wall2 = [build_ele.SecondSectWall2.value, build_ele.SecondSectWallLength2.value, build_ele.SecondSectWallPosit2.value, "SecondSectWallPosit2"]
        self.thi_sect_wall2 = [build_ele.ThirdSectWall2.value, build_ele.ThirdSectWallLength2.value, build_ele.ThirdSectWallPosit2.value, "ThirdSectWallPosit2"]
        self.fou_sect_wall2 = [build_ele.FourthSectWall2.value, build_ele.FourthSectWallLength2.value, build_ele.FourthSectWallPosit2.value, "FourthSectWallPosit22"]
        self.fif_sect_wall2 = [build_ele.FifthSectWall2.value, build_ele.FifthSectWallLength2.value, build_ele.FifthSectWallPosit2.value, "FifthSectWallPosit2"]
        self.six_sect_wall2 = [build_ele.SixthSectWall2.value, build_ele.SixthSectWallLength2.value, build_ele.SixthSectWallPosit2.value, "SixthSectWallPosit2"]
        self.sev_sect_wall2 = [build_ele.SeventhSectWall2.value, build_ele.SeventhSectWallLength2.value, build_ele.SeventhSectWallPosit2.value, "SeventhSectWallPosit2"]
        self.eig_sect_wall2 = [build_ele.EighthSectWall2.value, build_ele.EighthSectWallLength2.value, build_ele.EighthSectWallPosit2.value, "EighthSectWallPosit2"]
       
        self.fir_open2 = [build_ele.FirstOpening2.value, build_ele.FirstOpeningWidth2.value, build_ele.FirstOpeningHeight2.value,
                          build_ele.FirstOpeningXPosit2.value, build_ele.FirstOpeningZPosit2.value, "FirstOpeningXPosit2", "FirstOpeningWidth2"]
        self.sec_open2 = [build_ele.SecondOpening2.value, build_ele.SecondOpeningWidth2.value, build_ele.SecondOpeningHeight2.value,
                          build_ele.SecondOpeningXPosit2.value, build_ele.SecondOpeningZPosit2.value, "SecondOpeningXPosit2", "SecondOpeningWidth2"]
        self.thi_open2 = [build_ele.ThirdOpening2.value, build_ele.ThirdOpeningWidth2.value, build_ele.ThirdOpeningHeight2.value,
                          build_ele.ThirdOpeningXPosit2.value, build_ele.ThirdOpeningZPosit2.value, "ThirdOpeningXPosit2", "ThirdOpeningWidth2"]
        self.fou_open2 = [build_ele.FourthOpening2.value, build_ele.FourthOpeningWidth2.value, build_ele.FourthOpeningHeight2.value,
                          build_ele.FourthOpeningXPosit2.value, build_ele.FourthOpeningZPosit2.value, "FourthOpeningXPosit2", "FourthOpeningWidth2"]
        self.fif_open2 = [build_ele.FifthOpening2.value, build_ele.FifthOpeningWidth2.value, build_ele.FifthOpeningHeight2.value,
                          build_ele.FifthOpeningXPosit2.value, build_ele.FifthOpeningZPosit2.value, "FifthOpeningXPosit2", "FifthOpeningWidth2"]
        self.six_open2 = [build_ele.SixthOpening2.value, build_ele.SixthOpeningWidth2.value, build_ele.SixthOpeningHeight2.value,
                          build_ele.SixthOpeningXPosit2.value, build_ele.SixthOpeningZPosit2.value, "SixthOpeningXPosit2", "SixthOpeningWidth2"]      
        self.sev_open2 = [build_ele.SeventhOpening2.value, build_ele.SeventhOpeningWidth2.value, build_ele.SeventhOpeningHeight2.value,
                          build_ele.SeventhOpeningXPosit2.value, build_ele.SeventhOpeningZPosit2.value, "SeventhOpeningXPosit2", "SeventhOpeningWidth2"]
        self.eig_open2 = [build_ele.EighthOpening2.value, build_ele.EighthOpeningWidth2.value, build_ele.EighthOpeningHeight2.value,
                          build_ele.EighthOpeningXPosit2.value, build_ele.EighthOpeningZPosit2.value, "EighthOpeningXPosit2", "EighthOpeningWidth2"]
        self.nin_open2 = [build_ele.NinthOpening2.value, build_ele.NinthOpeningWidth2.value, build_ele.NinthOpeningHeight2.value,
                          build_ele.NinthOpeningXPosit2.value, build_ele.NinthOpeningZPosit2.value, "NinthOpeningXPosit2", "NinthOpeningWidth2"]
        self.ten_open2 = [build_ele.TenthOpening2.value, build_ele.TenthOpeningWidth2.value, build_ele.TenthOpeningHeight2.value,
                          build_ele.TenthOpeningXPosit2.value, build_ele.TenthOpeningZPosit2.value, "TenthOpeningXPosit2", "TenthOpeningWidth2"]
        self.ele_open2 = [build_ele.EleventhOpening2.value, build_ele.EleventhOpeningWidth2.value, build_ele.EleventhOpeningHeight2.value,
                          build_ele.EleventhOpeningXPosit2.value, build_ele.EleventhOpeningZPosit2.value, "EleventhOpeningXPosit2", "EleventhOpeningWidth2"]
        self.twe_open2 = [build_ele.TwelfthOpening2.value, build_ele.TwelfthOpeningWidth2.value, build_ele.TwelfthOpeningHeight2.value,
                          build_ele.TwelfthOpeningXPosit2.value, build_ele.TwelfthOpeningZPosit2.value, "TwelfthOpeningXPosit2", "TwelfthOpeningWidth2"]

        self.fir_door2 = [build_ele.FirstDoor2.value, build_ele.FirstDoorWidth2.value, build_ele.FirstDoorHeight2.value,
                          build_ele.FirstDoorXPosit2.value, build_ele.FirstDoorZPosit2.value, "FirstDoorXPosit2", "FirstDoorWidth2"]
        self.sec_door2 = [build_ele.SecondDoor2.value, build_ele.SecondDoorWidth2.value, build_ele.SecondDoorHeight2.value,
                          build_ele.SecondDoorXPosit2.value, build_ele.SecondDoorZPosit2.value, "SecondDoorXPosit2", "SecondDoorWidth2"]
        self.thi_door2 = [build_ele.ThirdDoor2.value, build_ele.ThirdDoorWidth2.value, build_ele.ThirdDoorHeight2.value,
                          build_ele.ThirdDoorXPosit2.value, build_ele.ThirdDoorZPosit2.value, "ThirdDoorXPosit2", "ThirdDoorWidth2"]
        self.fou_door2 = [build_ele.FourthDoor2.value, build_ele.FourthDoorWidth2.value, build_ele.FourthDoorHeight2.value,
                          build_ele.FourthDoorXPosit2.value, build_ele.FourthDoorZPosit2.value, "FourthDoorXPosit2", "FourthDoorWidth2"]
        self.fif_door2 = [build_ele.FifthDoor2.value, build_ele.FifthDoorWidth2.value, build_ele.FifthDoorHeight2.value,
                          build_ele.FifthDoorXPosit2.value, build_ele.FifthDoorZPosit2.value, "FifthDoorXPosit2", "FifthDoorWidth2"]
        self.six_door2 = [build_ele.SixthDoor2.value, build_ele.SixthDoorWidth2.value, build_ele.SixthDoorHeight2.value,
                          build_ele.SixthDoorXPosit2.value, build_ele.SixthDoorZPosit2.value, "SixthDoorXPosit2", "SixthDoorWidth2"]      
        self.sev_door2 = [build_ele.SeventhDoor2.value, build_ele.SeventhDoorWidth2.value, build_ele.SeventhDoorHeight2.value,
                          build_ele.SeventhDoorXPosit2.value, build_ele.SeventhDoorZPosit2.value, "SeventhDoorXPosit2", "SeventhDoorWidth2"]
        self.eig_door2 = [build_ele.EighthDoor2.value, build_ele.EighthDoorWidth2.value, build_ele.EighthDoorHeight2.value,
                          build_ele.EighthDoorXPosit2.value, build_ele.EighthDoorZPosit2.value, "EighthDoorXPosit2", "EighthDoorWidth2"]
        self.nin_door2 = [build_ele.NinthDoor2.value, build_ele.NinthDoorWidth2.value, build_ele.NinthDoorHeight2.value,
                          build_ele.NinthDoorXPosit2.value, build_ele.NinthDoorZPosit2.value, "NinthDoorXPosit2", "NinthDoorWidth2"]
        self.ten_door2 = [build_ele.TenthDoor2.value, build_ele.TenthDoorWidth2.value, build_ele.TenthDoorHeight2.value,
                          build_ele.TenthDoorXPosit2.value, build_ele.TenthDoorZPosit2.value, "TenthDoorXPosit2", "TenthDoorWidth2"]
        self.ele_door2 = [build_ele.EleventhDoor2.value, build_ele.EleventhDoorWidth2.value, build_ele.EleventhDoorHeight2.value,
                          build_ele.EleventhDoorXPosit2.value, build_ele.EleventhDoorZPosit2.value, "EleventhDoorXPosit2", "EleventhDoorWidth2"]
        self.twe_door2 = [build_ele.TwelfthDoor2.value, build_ele.TwelfthDoorWidth2.value, build_ele.TwelfthDoorHeight2.value,
                          build_ele.TwelfthDoorXPosit2.value, build_ele.TwelfthDoorZPosit2.value, "TwelfthDoorXPosit2", "TwelfthDoorWidth2"]

        self.open2 = [self.fir_open2, self.sec_open2, self.thi_open2, self.fou_open2, self.fif_open2, self.six_open2, 
                     self.sev_open2, self.eig_open2, self.nin_open2, self.ten_open2, self.ele_open2, self.twe_open2]
        self.door2 = [self.fir_door2, self.sec_door2, self.thi_door2, self.fou_door2, self.fif_door2, self.six_door2, 
                     self.sev_door2, self.eig_door2, self.nin_door2, self.ten_door2, self.ele_door2, self.twe_door2]

        for open, door in zip(self.open2, self.door2):
            if door[0]:
                for idx in range(len(door)):
                    open[idx] = door[idx]

        self.insul2 = [build_ele.CreateInsulation2.value, build_ele.InsulWidth.value, build_ele.InsulHeight.value, 
                       build_ele.InsulThick.value, build_ele.InsulMinWidth.value]
        self.insul_type2 = build_ele.ThrLayPanel2.value
        self.hor_rib_thick2, self.ver_rib_thick2  = build_ele.HorRibThick2.value, build_ele.VerRibThick2.value
        self.open_hor_rib_thick2, self.open_ver_rib_thick2 = build_ele.OpenHorRibThick2.value, build_ele.OpenVerRibThick2.value
        
        #-----------------------------------------------------------THIRD WALL----------------------------------------------------------------------
        self.create_wall3 = build_ele.CreateWall3.value
        self.wall3 = [build_ele.ModuleLength.value, build_ele.WallThick.value, "ModuleLength", None, None]
        self.left_end3 = [build_ele.LeftEnd3.value, build_ele.LeftEndLength3.value, build_ele.LeftPylonLength3.value]
        self.right_end3 = [build_ele.RightEnd3.value, build_ele.RightEndLength3.value, build_ele.RightPylonLength3.value]
        self.pylon_num3 = build_ele.PylonNum3.value  
        self.orient_params3 = [HandleDirection.x_dir, self.wall3[0], self.wall2[0], 180]
        
        self.fir_cent_pylon3 = [build_ele.FirstCentPylonLength3.value, build_ele.FirstCentPylonThick3.value, build_ele.FirstCentPylonPosit3.value, "FirstCentPylonPosit3"]
        self.sec_cent_pylon3 = [build_ele.SecondCentPylonLength3.value, build_ele.SecondCentPylonThick3.value, build_ele.SecondCentPylonPosit3.value, "SecondCentPylonPosit3"]
        self.thi_cent_pylon3 = [build_ele.ThirdCentPylonLength3.value, build_ele.ThirdCentPylonThick3.value, build_ele.ThirdCentPylonPosit3.value, "ThirdCentPylonPosit3"]

        self.fir_sect_wall3 = [build_ele.FirstSectWall3.value, build_ele.FirstSectWallLength3.value, build_ele.FirstSectWallPosit3.value, "FirstSectWallPosit3"]
        self.sec_sect_wall3 = [build_ele.SecondSectWall3.value, build_ele.SecondSectWallLength3.value, build_ele.SecondSectWallPosit3.value, "SecondSectWallPosit3"]
        self.thi_sect_wall3 = [build_ele.ThirdSectWall3.value, build_ele.ThirdSectWallLength3.value, build_ele.ThirdSectWallPosit3.value, "ThirdSectWallPosit3"]
        self.fou_sect_wall3 = [build_ele.FourthSectWall3.value, build_ele.FourthSectWallLength3.value, build_ele.FourthSectWallPosit3.value, "FourthSectWallPosit33"]
        self.fif_sect_wall3 = [build_ele.FifthSectWall3.value, build_ele.FifthSectWallLength3.value, build_ele.FifthSectWallPosit3.value, "FifthSectWallPosit3"]
        self.six_sect_wall3 = [build_ele.SixthSectWall3.value, build_ele.SixthSectWallLength3.value, build_ele.SixthSectWallPosit3.value, "SixthSectWallPosit3"]
        self.sev_sect_wall3 = [build_ele.SeventhSectWall3.value, build_ele.SeventhSectWallLength3.value, build_ele.SeventhSectWallPosit3.value, "SeventhSectWallPosit3"]
        self.eig_sect_wall3 = [build_ele.EighthSectWall3.value, build_ele.EighthSectWallLength3.value, build_ele.EighthSectWallPosit3.value, "EighthSectWallPosit3"]
       
        self.fir_open3 = [build_ele.FirstOpening3.value, build_ele.FirstOpeningWidth3.value, build_ele.FirstOpeningHeight3.value,
                          build_ele.FirstOpeningXPosit3.value, build_ele.FirstOpeningZPosit3.value, "FirstOpeningXPosit3", "FirstOpeningWidth3"]
        self.sec_open3 = [build_ele.SecondOpening3.value, build_ele.SecondOpeningWidth3.value, build_ele.SecondOpeningHeight3.value,
                          build_ele.SecondOpeningXPosit3.value, build_ele.SecondOpeningZPosit3.value, "SecondOpeningXPosit3", "SecondOpeningWidth3"]
        self.thi_open3 = [build_ele.ThirdOpening3.value, build_ele.ThirdOpeningWidth3.value, build_ele.ThirdOpeningHeight3.value,
                          build_ele.ThirdOpeningXPosit3.value, build_ele.ThirdOpeningZPosit3.value, "ThirdOpeningXPosit3", "ThirdOpeningWidth3"]
        self.fou_open3 = [build_ele.FourthOpening3.value, build_ele.FourthOpeningWidth3.value, build_ele.FourthOpeningHeight3.value,
                          build_ele.FourthOpeningXPosit3.value, build_ele.FourthOpeningZPosit3.value, "FourthOpeningXPosit3", "FourthOpeningWidth3"]
        self.fif_open3 = [build_ele.FifthOpening3.value, build_ele.FifthOpeningWidth3.value, build_ele.FifthOpeningHeight3.value,
                          build_ele.FifthOpeningXPosit3.value, build_ele.FifthOpeningZPosit3.value, "FifthOpeningXPosit3", "FifthOpeningWidth3"]
        self.six_open3 = [build_ele.SixthOpening3.value, build_ele.SixthOpeningWidth3.value, build_ele.SixthOpeningHeight3.value,
                          build_ele.SixthOpeningXPosit3.value, build_ele.SixthOpeningZPosit3.value, "SixthOpeningXPosit3", "SixthOpeningWidth3"]      
        self.sev_open3 = [build_ele.SeventhOpening3.value, build_ele.SeventhOpeningWidth3.value, build_ele.SeventhOpeningHeight3.value,
                          build_ele.SeventhOpeningXPosit3.value, build_ele.SeventhOpeningZPosit3.value, "SeventhOpeningXPosit3", "SeventhOpeningWidth3"]
        self.eig_open3 = [build_ele.EighthOpening3.value, build_ele.EighthOpeningWidth3.value, build_ele.EighthOpeningHeight3.value,
                          build_ele.EighthOpeningXPosit3.value, build_ele.EighthOpeningZPosit3.value, "EighthOpeningXPosit3", "EighthOpeningWidth3"]
        self.nin_open3 = [build_ele.NinthOpening3.value, build_ele.NinthOpeningWidth3.value, build_ele.NinthOpeningHeight3.value,
                          build_ele.NinthOpeningXPosit3.value, build_ele.NinthOpeningZPosit3.value, "NinthOpeningXPosit3", "NinthOpeningWidth3"]
        self.ten_open3 = [build_ele.TenthOpening3.value, build_ele.TenthOpeningWidth3.value, build_ele.TenthOpeningHeight3.value,
                          build_ele.TenthOpeningXPosit3.value, build_ele.TenthOpeningZPosit3.value, "TenthOpeningXPosit3", "TenthOpeningWidth3"]
        self.ele_open3 = [build_ele.EleventhOpening3.value, build_ele.EleventhOpeningWidth3.value, build_ele.EleventhOpeningHeight3.value,
                          build_ele.EleventhOpeningXPosit3.value, build_ele.EleventhOpeningZPosit3.value, "EleventhOpeningXPosit3", "EleventhOpeningWidth3"]
        self.twe_open3 = [build_ele.TwelfthOpening3.value, build_ele.TwelfthOpeningWidth3.value, build_ele.TwelfthOpeningHeight3.value,
                          build_ele.TwelfthOpeningXPosit3.value, build_ele.TwelfthOpeningZPosit3.value, "TwelfthOpeningXPosit3", "TwelfthOpeningWidth3"]

        self.fir_door3 = [build_ele.FirstDoor3.value, build_ele.FirstDoorWidth3.value, build_ele.FirstDoorHeight3.value,
                          build_ele.FirstDoorXPosit3.value, build_ele.FirstDoorZPosit3.value, "FirstDoorXPosit3", "FirstDoorWidth3"]
        self.sec_door3 = [build_ele.SecondDoor3.value, build_ele.SecondDoorWidth3.value, build_ele.SecondDoorHeight3.value,
                          build_ele.SecondDoorXPosit3.value, build_ele.SecondDoorZPosit3.value, "SecondDoorXPosit3", "SecondDoorWidth3"]
        self.thi_door3 = [build_ele.ThirdDoor3.value, build_ele.ThirdDoorWidth3.value, build_ele.ThirdDoorHeight3.value,
                          build_ele.ThirdDoorXPosit3.value, build_ele.ThirdDoorZPosit3.value, "ThirdDoorXPosit3", "ThirdDoorWidth3"]
        self.fou_door3 = [build_ele.FourthDoor3.value, build_ele.FourthDoorWidth3.value, build_ele.FourthDoorHeight3.value,
                          build_ele.FourthDoorXPosit3.value, build_ele.FourthDoorZPosit3.value, "FourthDoorXPosit3", "FourthDoorWidth3"]
        self.fif_door3 = [build_ele.FifthDoor3.value, build_ele.FifthDoorWidth3.value, build_ele.FifthDoorHeight3.value,
                          build_ele.FifthDoorXPosit3.value, build_ele.FifthDoorZPosit3.value, "FifthDoorXPosit3", "FifthDoorWidth3"]
        self.six_door3 = [build_ele.SixthDoor3.value, build_ele.SixthDoorWidth3.value, build_ele.SixthDoorHeight3.value,
                          build_ele.SixthDoorXPosit3.value, build_ele.SixthDoorZPosit3.value, "SixthDoorXPosit3", "SixthDoorWidth3"]      
        self.sev_door3 = [build_ele.SeventhDoor3.value, build_ele.SeventhDoorWidth3.value, build_ele.SeventhDoorHeight3.value,
                          build_ele.SeventhDoorXPosit3.value, build_ele.SeventhDoorZPosit3.value, "SeventhDoorXPosit3", "SeventhDoorWidth3"]
        self.eig_door3 = [build_ele.EighthDoor3.value, build_ele.EighthDoorWidth3.value, build_ele.EighthDoorHeight3.value,
                          build_ele.EighthDoorXPosit3.value, build_ele.EighthDoorZPosit3.value, "EighthDoorXPosit3", "EighthDoorWidth3"]
        self.nin_door3 = [build_ele.NinthDoor3.value, build_ele.NinthDoorWidth3.value, build_ele.NinthDoorHeight3.value,
                          build_ele.NinthDoorXPosit3.value, build_ele.NinthDoorZPosit3.value, "NinthDoorXPosit3", "NinthDoorWidth3"]
        self.ten_door3 = [build_ele.TenthDoor3.value, build_ele.TenthDoorWidth3.value, build_ele.TenthDoorHeight3.value,
                          build_ele.TenthDoorXPosit3.value, build_ele.TenthDoorZPosit3.value, "TenthDoorXPosit3", "TenthDoorWidth3"]
        self.ele_door3 = [build_ele.EleventhDoor3.value, build_ele.EleventhDoorWidth3.value, build_ele.EleventhDoorHeight3.value,
                          build_ele.EleventhDoorXPosit3.value, build_ele.EleventhDoorZPosit3.value, "EleventhDoorXPosit3", "EleventhDoorWidth3"]
        self.twe_door3 = [build_ele.TwelfthDoor3.value, build_ele.TwelfthDoorWidth3.value, build_ele.TwelfthDoorHeight3.value,
                          build_ele.TwelfthDoorXPosit3.value, build_ele.TwelfthDoorZPosit3.value, "TwelfthDoorXPosit3", "TwelfthDoorWidth3"]

        self.open3 = [self.fir_open3, self.sec_open3, self.thi_open3, self.fou_open3, self.fif_open3, self.six_open3, 
                     self.sev_open3, self.eig_open3, self.nin_open3, self.ten_open3, self.ele_open3, self.twe_open3]
        self.door3 = [self.fir_door3, self.sec_door3, self.thi_door3, self.fou_door3, self.fif_door3, self.six_door3, 
                     self.sev_door3, self.eig_door3, self.nin_door3, self.ten_door3, self.ele_door3, self.twe_door3]

        for open, door in zip(self.open3, self.door3):
            if door[0]:
                for idx in range(len(door)):
                    open[idx] = door[idx]

        self.insul3 = [build_ele.CreateInsulation3.value, build_ele.InsulWidth.value, build_ele.InsulHeight.value, 
                       build_ele.InsulThick.value, build_ele.InsulMinWidth.value]
        self.insul_type3 = build_ele.ThrLayPanel3.value
        self.hor_rib_thick3, self.ver_rib_thick3  = build_ele.HorRibThick3.value, build_ele.VerRibThick3.value
        self.open_hor_rib_thick3, self.open_ver_rib_thick3 = build_ele.OpenHorRibThick3.value, build_ele.OpenVerRibThick3.value

        #-----------------------------------------------------------FOURTH WALL---------------------------------------------------------------------
        self.create_wall4 = build_ele.CreateWall4.value
        self.wall4 = [build_ele.ModuleWidth.value, build_ele.WallThick.value, "ModuleWidth", None, None]
        self.left_end4 = [build_ele.LeftEnd4.value, build_ele.LeftEndLength4.value, build_ele.LeftPylonLength4.value]
        self.right_end4 = [build_ele.RightEnd4.value, build_ele.RightEndLength4.value, build_ele.RightPylonLength4.value]
        self.pylon_num4 = build_ele.PylonNum4.value 
        self.orient_params4 = [HandleDirection.y_dir, 0, self.wall4[0], 270]

        self.fir_cent_pylon4 = [build_ele.FirstCentPylonLength4.value, build_ele.FirstCentPylonThick4.value, build_ele.FirstCentPylonPosit4.value, "FirstCentPylonPosit4"]
        self.sec_cent_pylon4 = [build_ele.SecondCentPylonLength4.value, build_ele.SecondCentPylonThick4.value, build_ele.SecondCentPylonPosit4.value, "SecondCentPylonPosit4"]
        self.thi_cent_pylon4 = [build_ele.ThirdCentPylonLength4.value, build_ele.ThirdCentPylonThick4.value, build_ele.ThirdCentPylonPosit4.value, "ThirdCentPylonPosit4"]

        self.fir_sect_wall4 = [build_ele.FirstSectWall4.value, build_ele.FirstSectWallLength4.value, build_ele.FirstSectWallPosit4.value, "FirstSectWallPosit4"]
        self.sec_sect_wall4 = [build_ele.SecondSectWall4.value, build_ele.SecondSectWallLength4.value, build_ele.SecondSectWallPosit4.value, "SecondSectWallPosit4"]
        self.thi_sect_wall4 = [build_ele.ThirdSectWall4.value, build_ele.ThirdSectWallLength4.value, build_ele.ThirdSectWallPosit4.value, "ThirdSectWallPosit4"]
        self.fou_sect_wall4 = [build_ele.FourthSectWall4.value, build_ele.FourthSectWallLength4.value, build_ele.FourthSectWallPosit4.value, "FourthSectWallPosit44"]
        self.fif_sect_wall4 = [build_ele.FifthSectWall4.value, build_ele.FifthSectWallLength4.value, build_ele.FifthSectWallPosit4.value, "FifthSectWallPosit4"]
        self.six_sect_wall4 = [build_ele.SixthSectWall4.value, build_ele.SixthSectWallLength4.value, build_ele.SixthSectWallPosit4.value, "SixthSectWallPosit4"]
        self.sev_sect_wall4 = [build_ele.SeventhSectWall4.value, build_ele.SeventhSectWallLength4.value, build_ele.SeventhSectWallPosit4.value, "SeventhSectWallPosit4"]
        self.eig_sect_wall4 = [build_ele.EighthSectWall4.value, build_ele.EighthSectWallLength4.value, build_ele.EighthSectWallPosit4.value, "EighthSectWallPosit4"]
   
        self.fir_open4 = [build_ele.FirstOpening4.value, build_ele.FirstOpeningWidth4.value, build_ele.FirstOpeningHeight4.value,
                          build_ele.FirstOpeningXPosit4.value, build_ele.FirstOpeningZPosit4.value, "FirstOpeningXPosit4", "FirstOpeningWidth4"]
        self.sec_open4 = [build_ele.SecondOpening4.value, build_ele.SecondOpeningWidth4.value, build_ele.SecondOpeningHeight4.value,
                          build_ele.SecondOpeningXPosit4.value, build_ele.SecondOpeningZPosit4.value, "SecondOpeningXPosit4", "SecondOpeningWidth4"]
        self.thi_open4 = [build_ele.ThirdOpening4.value, build_ele.ThirdOpeningWidth4.value, build_ele.ThirdOpeningHeight4.value,
                          build_ele.ThirdOpeningXPosit4.value, build_ele.ThirdOpeningZPosit4.value, "ThirdOpeningXPosit4", "ThirdOpeningWidth4"]
        self.fou_open4 = [build_ele.FourthOpening4.value, build_ele.FourthOpeningWidth4.value, build_ele.FourthOpeningHeight4.value,
                          build_ele.FourthOpeningXPosit4.value, build_ele.FourthOpeningZPosit4.value, "FourthOpeningXPosit4", "FourthOpeningWidth4"]
        self.fif_open4 = [build_ele.FifthOpening4.value, build_ele.FifthOpeningWidth4.value, build_ele.FifthOpeningHeight4.value,
                          build_ele.FifthOpeningXPosit4.value, build_ele.FifthOpeningZPosit4.value, "FifthOpeningXPosit4", "FifthOpeningWidth4"]
        self.six_open4 = [build_ele.SixthOpening4.value, build_ele.SixthOpeningWidth4.value, build_ele.SixthOpeningHeight4.value,
                          build_ele.SixthOpeningXPosit4.value, build_ele.SixthOpeningZPosit4.value, "SixthOpeningXPosit4", "SixthOpeningWidth4"]      
        self.sev_open4 = [build_ele.SeventhOpening4.value, build_ele.SeventhOpeningWidth4.value, build_ele.SeventhOpeningHeight4.value,
                          build_ele.SeventhOpeningXPosit4.value, build_ele.SeventhOpeningZPosit4.value, "SeventhOpeningXPosit4", "SeventhOpeningWidth4"]
        self.eig_open4 = [build_ele.EighthOpening4.value, build_ele.EighthOpeningWidth4.value, build_ele.EighthOpeningHeight4.value,
                          build_ele.EighthOpeningXPosit4.value, build_ele.EighthOpeningZPosit4.value, "EighthOpeningXPosit4", "EighthOpeningWidth4"]
        self.nin_open4 = [build_ele.NinthOpening4.value, build_ele.NinthOpeningWidth4.value, build_ele.NinthOpeningHeight4.value,
                          build_ele.NinthOpeningXPosit4.value, build_ele.NinthOpeningZPosit4.value, "NinthOpeningXPosit4", "NinthOpeningWidth4"]
        self.ten_open4 = [build_ele.TenthOpening4.value, build_ele.TenthOpeningWidth4.value, build_ele.TenthOpeningHeight4.value,
                          build_ele.TenthOpeningXPosit4.value, build_ele.TenthOpeningZPosit4.value, "TenthOpeningXPosit4", "TenthOpeningWidth4"]
        self.ele_open4 = [build_ele.EleventhOpening4.value, build_ele.EleventhOpeningWidth4.value, build_ele.EleventhOpeningHeight4.value,
                          build_ele.EleventhOpeningXPosit4.value, build_ele.EleventhOpeningZPosit4.value, "EleventhOpeningXPosit4", "EleventhOpeningWidth4"]
        self.twe_open4 = [build_ele.TwelfthOpening4.value, build_ele.TwelfthOpeningWidth4.value, build_ele.TwelfthOpeningHeight4.value,
                          build_ele.TwelfthOpeningXPosit4.value, build_ele.TwelfthOpeningZPosit4.value, "TwelfthOpeningXPosit4", "TwelfthOpeningWidth4"]

        self.fir_door4 = [build_ele.FirstDoor4.value, build_ele.FirstDoorWidth4.value, build_ele.FirstDoorHeight4.value,
                          build_ele.FirstDoorXPosit4.value, build_ele.FirstDoorZPosit4.value, "FirstDoorXPosit4", "FirstDoorWidth4"]
        self.sec_door4 = [build_ele.SecondDoor4.value, build_ele.SecondDoorWidth4.value, build_ele.SecondDoorHeight4.value,
                          build_ele.SecondDoorXPosit4.value, build_ele.SecondDoorZPosit4.value, "SecondDoorXPosit4", "SecondDoorWidth4"]
        self.thi_door4 = [build_ele.ThirdDoor4.value, build_ele.ThirdDoorWidth4.value, build_ele.ThirdDoorHeight4.value,
                          build_ele.ThirdDoorXPosit4.value, build_ele.ThirdDoorZPosit4.value, "ThirdDoorXPosit4", "ThirdDoorWidth4"]
        self.fou_door4 = [build_ele.FourthDoor4.value, build_ele.FourthDoorWidth4.value, build_ele.FourthDoorHeight4.value,
                          build_ele.FourthDoorXPosit4.value, build_ele.FourthDoorZPosit4.value, "FourthDoorXPosit4", "FourthDoorWidth4"]
        self.fif_door4 = [build_ele.FifthDoor4.value, build_ele.FifthDoorWidth4.value, build_ele.FifthDoorHeight4.value,
                          build_ele.FifthDoorXPosit4.value, build_ele.FifthDoorZPosit4.value, "FifthDoorXPosit4", "FifthDoorWidth4"]
        self.six_door4 = [build_ele.SixthDoor4.value, build_ele.SixthDoorWidth4.value, build_ele.SixthDoorHeight4.value,
                          build_ele.SixthDoorXPosit4.value, build_ele.SixthDoorZPosit4.value, "SixthDoorXPosit4", "SixthDoorWidth4"]      
        self.sev_door4 = [build_ele.SeventhDoor4.value, build_ele.SeventhDoorWidth4.value, build_ele.SeventhDoorHeight4.value,
                          build_ele.SeventhDoorXPosit4.value, build_ele.SeventhDoorZPosit4.value, "SeventhDoorXPosit4", "SeventhDoorWidth4"]
        self.eig_door4 = [build_ele.EighthDoor4.value, build_ele.EighthDoorWidth4.value, build_ele.EighthDoorHeight4.value,
                          build_ele.EighthDoorXPosit4.value, build_ele.EighthDoorZPosit4.value, "EighthDoorXPosit4", "EighthDoorWidth4"]
        self.nin_door4 = [build_ele.NinthDoor4.value, build_ele.NinthDoorWidth4.value, build_ele.NinthDoorHeight4.value,
                          build_ele.NinthDoorXPosit4.value, build_ele.NinthDoorZPosit4.value, "NinthDoorXPosit4", "NinthDoorWidth4"]
        self.ten_door4 = [build_ele.TenthDoor4.value, build_ele.TenthDoorWidth4.value, build_ele.TenthDoorHeight4.value,
                          build_ele.TenthDoorXPosit4.value, build_ele.TenthDoorZPosit4.value, "TenthDoorXPosit4", "TenthDoorWidth4"]
        self.ele_door4 = [build_ele.EleventhDoor4.value, build_ele.EleventhDoorWidth4.value, build_ele.EleventhDoorHeight4.value,
                          build_ele.EleventhDoorXPosit4.value, build_ele.EleventhDoorZPosit4.value, "EleventhDoorXPosit4", "EleventhDoorWidth4"]
        self.twe_door4 = [build_ele.TwelfthDoor4.value, build_ele.TwelfthDoorWidth4.value, build_ele.TwelfthDoorHeight4.value,
                          build_ele.TwelfthDoorXPosit4.value, build_ele.TwelfthDoorZPosit4.value, "TwelfthDoorXPosit4", "TwelfthDoorWidth4"]

        self.open4 = [self.fir_open4, self.sec_open4, self.thi_open4, self.fou_open4, self.fif_open4, self.six_open4, 
                     self.sev_open4, self.eig_open4, self.nin_open4, self.ten_open4, self.ele_open4, self.twe_open4]
        self.door4 = [self.fir_door4, self.sec_door4, self.thi_door4, self.fou_door4, self.fif_door4, self.six_door4, 
                     self.sev_door4, self.eig_door4, self.nin_door4, self.ten_door4, self.ele_door4, self.twe_door4]

        for open, door in zip(self.open4, self.door4):
            if door[0]:
                for idx in range(len(door)):
                    open[idx] = door[idx]

        self.insul4 = [build_ele.CreateInsulation4.value, build_ele.InsulWidth.value, build_ele.InsulHeight.value, 
                       build_ele.InsulThick.value, build_ele.InsulMinWidth.value]
        self.insul_type4 = build_ele.ThrLayPanel4.value
        self.hor_rib_thick4, self.ver_rib_thick4  = build_ele.HorRibThick4.value, build_ele.VerRibThick4.value
        self.open_hor_rib_thick4, self.open_ver_rib_thick4 = build_ele.OpenHorRibThick4.value, build_ele.OpenVerRibThick4.value
 
        #-----------------------------------------------------------FIFTH WALL----------------------------------------------------------------------
        self.create_wall5 = build_ele.CreateWall5.value
        self.wall5 = [build_ele.WallLength5.value, build_ele.WallThick5.value, "WallLength5", build_ele.LeftEndOffset5.value, "LeftEndOffset5"]
        self.left_end5 = [build_ele.LeftEnd5.value, build_ele.LeftEndLength5.value, None]
        self.right_end5 = [build_ele.RightEnd5.value, build_ele.RightEndLength5.value, None]
        self.pylon_num5 = build_ele.PylonNum5.value 
        self.wall_offset5 = [build_ele.WallOffset5.value, "WallOffset5"]
        self.wall_inverse5 =  build_ele.WallInverse5.value
        if not self.wall_inverse5:
            self.orient_params5 = [HandleDirection.x_dir, 0, self.wall_offset5[0], 0]
            self.orient_params5_1 = [HandleDirection.y_dir, self.wall5[3], self.wall5[1], 90]
        else:
            self.orient_params5 = [HandleDirection.x_dir, self.wall1[0], self.wall_offset5[0], 180]
            self.orient_params5_1 = [HandleDirection.y_dir, self.wall1[0] - self.wall5[3], -self.wall5[1], 90]
        
        self.fir_cent_pylon5 = [build_ele.FirstCentPylonLength5.value, build_ele.FirstCentPylonThick5.value, build_ele.FirstCentPylonPosit5.value, "FirstCentPylonPosit5"]
        self.sec_cent_pylon5 = [build_ele.SecondCentPylonLength5.value, build_ele.SecondCentPylonThick5.value, build_ele.SecondCentPylonPosit5.value, "SecondCentPylonPosit5"]
        self.thi_cent_pylon5 = [build_ele.ThirdCentPylonLength5.value, build_ele.ThirdCentPylonThick5.value, build_ele.ThirdCentPylonPosit5.value, "ThirdCentPylonPosit5"]

        self.fir_sect_wall5 = [build_ele.FirstSectWall5.value, build_ele.FirstSectWallLength5.value, build_ele.FirstSectWallPosit5.value, "FirstSectWallPosit5"]
        self.sec_sect_wall5 = [build_ele.SecondSectWall5.value, build_ele.SecondSectWallLength5.value, build_ele.SecondSectWallPosit5.value, "SecondSectWallPosit5"]
        self.thi_sect_wall5 = [build_ele.ThirdSectWall5.value, build_ele.ThirdSectWallLength5.value, build_ele.ThirdSectWallPosit5.value, "ThirdSectWallPosit5"]
        self.fou_sect_wall5 = [build_ele.FourthSectWall5.value, build_ele.FourthSectWallLength5.value, build_ele.FourthSectWallPosit5.value, "FourthSectWallPosit55"]
        self.fif_sect_wall5 = [build_ele.FifthSectWall5.value, build_ele.FifthSectWallLength5.value, build_ele.FifthSectWallPosit5.value, "FifthSectWallPosit5"]
        self.six_sect_wall5 = [build_ele.SixthSectWall5.value, build_ele.SixthSectWallLength5.value, build_ele.SixthSectWallPosit5.value, "SixthSectWallPosit5"]
        self.sev_sect_wall5 = [build_ele.SeventhSectWall5.value, build_ele.SeventhSectWallLength5.value, build_ele.SeventhSectWallPosit5.value, "SeventhSectWallPosit5"]
        self.eig_sect_wall5 = [build_ele.EighthSectWall5.value, build_ele.EighthSectWallLength5.value, build_ele.EighthSectWallPosit5.value, "EighthSectWallPosit5"]
       
        self.fir_open5 = [build_ele.FirstOpening5.value, build_ele.FirstOpeningWidth5.value, build_ele.FirstOpeningHeight5.value,
                          build_ele.FirstOpeningXPosit5.value, build_ele.FirstOpeningZPosit5.value, "FirstOpeningXPosit5", "FirstOpeningWidth5"]
        self.sec_open5 = [build_ele.SecondOpening5.value, build_ele.SecondOpeningWidth5.value, build_ele.SecondOpeningHeight5.value,
                          build_ele.SecondOpeningXPosit5.value, build_ele.SecondOpeningZPosit5.value, "SecondOpeningXPosit5", "SecondOpeningWidth5"]
        self.thi_open5 = [build_ele.ThirdOpening5.value, build_ele.ThirdOpeningWidth5.value, build_ele.ThirdOpeningHeight5.value,
                          build_ele.ThirdOpeningXPosit5.value, build_ele.ThirdOpeningZPosit5.value, "ThirdOpeningXPosit5", "ThirdOpeningWidth5"]
        self.fou_open5 = [build_ele.FourthOpening5.value, build_ele.FourthOpeningWidth5.value, build_ele.FourthOpeningHeight5.value,
                          build_ele.FourthOpeningXPosit5.value, build_ele.FourthOpeningZPosit5.value, "FourthOpeningXPosit5", "FourthOpeningWidth5"]
        self.fif_open5 = [build_ele.FifthOpening5.value, build_ele.FifthOpeningWidth5.value, build_ele.FifthOpeningHeight5.value,
                          build_ele.FifthOpeningXPosit5.value, build_ele.FifthOpeningZPosit5.value, "FifthOpeningXPosit5", "FifthOpeningWidth5"]
        self.six_open5 = [build_ele.SixthOpening5.value, build_ele.SixthOpeningWidth5.value, build_ele.SixthOpeningHeight5.value,
                          build_ele.SixthOpeningXPosit5.value, build_ele.SixthOpeningZPosit5.value, "SixthOpeningXPosit5", "SixthOpeningWidth5"]      
        self.sev_open5 = [build_ele.SeventhOpening5.value, build_ele.SeventhOpeningWidth5.value, build_ele.SeventhOpeningHeight5.value,
                          build_ele.SeventhOpeningXPosit5.value, build_ele.SeventhOpeningZPosit5.value, "SeventhOpeningXPosit5", "SeventhOpeningWidth5"]
        self.eig_open5 = [build_ele.EighthOpening5.value, build_ele.EighthOpeningWidth5.value, build_ele.EighthOpeningHeight5.value,
                          build_ele.EighthOpeningXPosit5.value, build_ele.EighthOpeningZPosit5.value, "EighthOpeningXPosit5", "EighthOpeningWidth5"]
        self.nin_open5 = [build_ele.NinthOpening5.value, build_ele.NinthOpeningWidth5.value, build_ele.NinthOpeningHeight5.value,
                          build_ele.NinthOpeningXPosit5.value, build_ele.NinthOpeningZPosit5.value, "NinthOpeningXPosit5", "NinthOpeningWidth5"]
        self.ten_open5 = [build_ele.TenthOpening5.value, build_ele.TenthOpeningWidth5.value, build_ele.TenthOpeningHeight5.value,
                          build_ele.TenthOpeningXPosit5.value, build_ele.TenthOpeningZPosit5.value, "TenthOpeningXPosit5", "TenthOpeningWidth5"]
        self.ele_open5 = [build_ele.EleventhOpening5.value, build_ele.EleventhOpeningWidth5.value, build_ele.EleventhOpeningHeight5.value,
                          build_ele.EleventhOpeningXPosit5.value, build_ele.EleventhOpeningZPosit5.value, "EleventhOpeningXPosit5", "EleventhOpeningWidth5"]
        self.twe_open5 = [build_ele.TwelfthOpening5.value, build_ele.TwelfthOpeningWidth5.value, build_ele.TwelfthOpeningHeight5.value,
                          build_ele.TwelfthOpeningXPosit5.value, build_ele.TwelfthOpeningZPosit5.value, "TwelfthOpeningXPosit5", "TwelfthOpeningWidth5"]

        self.fir_door5 = [build_ele.FirstDoor5.value, build_ele.FirstDoorWidth5.value, build_ele.FirstDoorHeight5.value,
                          build_ele.FirstDoorXPosit5.value, build_ele.FirstDoorZPosit5.value, "FirstDoorXPosit5", "FirstDoorWidth5"]
        self.sec_door5 = [build_ele.SecondDoor5.value, build_ele.SecondDoorWidth5.value, build_ele.SecondDoorHeight5.value,
                          build_ele.SecondDoorXPosit5.value, build_ele.SecondDoorZPosit5.value, "SecondDoorXPosit5", "SecondDoorWidth5"]
        self.thi_door5 = [build_ele.ThirdDoor5.value, build_ele.ThirdDoorWidth5.value, build_ele.ThirdDoorHeight5.value,
                          build_ele.ThirdDoorXPosit5.value, build_ele.ThirdDoorZPosit5.value, "ThirdDoorXPosit5", "ThirdDoorWidth5"]
        self.fou_door5 = [build_ele.FourthDoor5.value, build_ele.FourthDoorWidth5.value, build_ele.FourthDoorHeight5.value,
                          build_ele.FourthDoorXPosit5.value, build_ele.FourthDoorZPosit5.value, "FourthDoorXPosit5", "FourthDoorWidth5"]
        self.fif_door5 = [build_ele.FifthDoor5.value, build_ele.FifthDoorWidth5.value, build_ele.FifthDoorHeight5.value,
                          build_ele.FifthDoorXPosit5.value, build_ele.FifthDoorZPosit5.value, "FifthDoorXPosit5", "FifthDoorWidth5"]
        self.six_door5 = [build_ele.SixthDoor5.value, build_ele.SixthDoorWidth5.value, build_ele.SixthDoorHeight5.value,
                          build_ele.SixthDoorXPosit5.value, build_ele.SixthDoorZPosit5.value, "SixthDoorXPosit5", "SixthDoorWidth5"]      
        self.sev_door5 = [build_ele.SeventhDoor5.value, build_ele.SeventhDoorWidth5.value, build_ele.SeventhDoorHeight5.value,
                          build_ele.SeventhDoorXPosit5.value, build_ele.SeventhDoorZPosit5.value, "SeventhDoorXPosit5", "SeventhDoorWidth5"]
        self.eig_door5 = [build_ele.EighthDoor5.value, build_ele.EighthDoorWidth5.value, build_ele.EighthDoorHeight5.value,
                          build_ele.EighthDoorXPosit5.value, build_ele.EighthDoorZPosit5.value, "EighthDoorXPosit5", "EighthDoorWidth5"]
        self.nin_door5 = [build_ele.NinthDoor5.value, build_ele.NinthDoorWidth5.value, build_ele.NinthDoorHeight5.value,
                          build_ele.NinthDoorXPosit5.value, build_ele.NinthDoorZPosit5.value, "NinthDoorXPosit5", "NinthDoorWidth5"]
        self.ten_door5 = [build_ele.TenthDoor5.value, build_ele.TenthDoorWidth5.value, build_ele.TenthDoorHeight5.value,
                          build_ele.TenthDoorXPosit5.value, build_ele.TenthDoorZPosit5.value, "TenthDoorXPosit5", "TenthDoorWidth5"]
        self.ele_door5 = [build_ele.EleventhDoor5.value, build_ele.EleventhDoorWidth5.value, build_ele.EleventhDoorHeight5.value,
                          build_ele.EleventhDoorXPosit5.value, build_ele.EleventhDoorZPosit5.value, "EleventhDoorXPosit5", "EleventhDoorWidth5"]
        self.twe_door5 = [build_ele.TwelfthDoor5.value, build_ele.TwelfthDoorWidth5.value, build_ele.TwelfthDoorHeight5.value,
                          build_ele.TwelfthDoorXPosit5.value, build_ele.TwelfthDoorZPosit5.value, "TwelfthDoorXPosit5", "TwelfthDoorWidth5"]

        self.open5 = [self.fir_open5, self.sec_open5, self.thi_open5, self.fou_open5, self.fif_open5, self.six_open5, 
                     self.sev_open5, self.eig_open5, self.nin_open5, self.ten_open5, self.ele_open5, self.twe_open5]
        self.door5 = [self.fir_door5, self.sec_door5, self.thi_door5, self.fou_door5, self.fif_door5, self.six_door5, 
                     self.sev_door5, self.eig_door5, self.nin_door5, self.ten_door5, self.ele_door5, self.twe_door5]

        for open, door in zip(self.open5, self.door5):
            if door[0]:
                for idx in range(len(door)):
                    open[idx] = door[idx]

        self.insul5 = [build_ele.CreateInsulation5.value, build_ele.InsulWidth.value, build_ele.InsulHeight.value, 
                       build_ele.InsulThick.value, build_ele.InsulMinWidth.value]
        self.insul_type5 = build_ele.ThrLayPanel5.value
        self.hor_rib_thick5, self.ver_rib_thick5  = build_ele.HorRibThick5.value, build_ele.VerRibThick5.value
        self.open_hor_rib_thick5, self.open_ver_rib_thick5 = build_ele.OpenHorRibThick5.value, build_ele.OpenVerRibThick5.value
            
        #-----------------------------------------------------------SIXTH WALL----------------------------------------------------------------------
        self.create_wall6 = build_ele.CreateWall6.value
        self.wall6 = [build_ele.WallLength6.value, build_ele.WallThick6.value, "WallLength6", build_ele.LeftEndOffset6.value, "LeftEndOffset6"]
        self.left_end6 = [build_ele.LeftEnd6.value, build_ele.LeftEndLength6.value, None]
        self.right_end6 = [build_ele.RightEnd6.value, build_ele.RightEndLength6.value, None]
        self.pylon_num6 = build_ele.PylonNum6.value 
        self.wall_offset6 = [build_ele.WallOffset6.value, "WallOffset6"]
        self.wall_inverse6 = build_ele.WallInverse6.value
        if not self.wall_inverse6:
            self.orient_params6 = [HandleDirection.x_dir, 0, self.wall_offset6[0], 0]
            self.orient_params6_1 = [HandleDirection.y_dir, self.wall6[3], self.wall6[1], 90]
        else:
            self.orient_params6 = [HandleDirection.x_dir, self.wall1[0], self.wall_offset6[0], 180]
            self.orient_params6_1 = [HandleDirection.y_dir, self.wall1[0] - self.wall6[3], -self.wall6[1], 90]
        
        self.fir_cent_pylon6 = [build_ele.FirstCentPylonLength6.value, build_ele.FirstCentPylonThick6.value, build_ele.FirstCentPylonPosit6.value, "FirstCentPylonPosit6"]
        self.sec_cent_pylon6 = [build_ele.SecondCentPylonLength6.value, build_ele.SecondCentPylonThick6.value, build_ele.SecondCentPylonPosit6.value, "SecondCentPylonPosit6"]
        self.thi_cent_pylon6 = [build_ele.ThirdCentPylonLength6.value, build_ele.ThirdCentPylonThick6.value, build_ele.ThirdCentPylonPosit6.value, "ThirdCentPylonPosit6"]

        self.fir_sect_wall6 = [build_ele.FirstSectWall6.value, build_ele.FirstSectWallLength6.value, build_ele.FirstSectWallPosit6.value, "FirstSectWallPosit6"]
        self.sec_sect_wall6 = [build_ele.SecondSectWall6.value, build_ele.SecondSectWallLength6.value, build_ele.SecondSectWallPosit6.value, "SecondSectWallPosit6"]
        self.thi_sect_wall6 = [build_ele.ThirdSectWall6.value, build_ele.ThirdSectWallLength6.value, build_ele.ThirdSectWallPosit6.value, "ThirdSectWallPosit6"]
        self.fou_sect_wall6 = [build_ele.FourthSectWall6.value, build_ele.FourthSectWallLength6.value, build_ele.FourthSectWallPosit6.value, "FourthSectWallPosit66"]
        self.fif_sect_wall6 = [build_ele.FifthSectWall6.value, build_ele.FifthSectWallLength6.value, build_ele.FifthSectWallPosit6.value, "FifthSectWallPosit6"]
        self.six_sect_wall6 = [build_ele.SixthSectWall6.value, build_ele.SixthSectWallLength6.value, build_ele.SixthSectWallPosit6.value, "SixthSectWallPosit6"]
        self.sev_sect_wall6 = [build_ele.SeventhSectWall6.value, build_ele.SeventhSectWallLength6.value, build_ele.SeventhSectWallPosit6.value, "SeventhSectWallPosit6"]
        self.eig_sect_wall6 = [build_ele.EighthSectWall6.value, build_ele.EighthSectWallLength6.value, build_ele.EighthSectWallPosit6.value, "EighthSectWallPosit6"]
       
        self.fir_open6 = [build_ele.FirstOpening6.value, build_ele.FirstOpeningWidth6.value, build_ele.FirstOpeningHeight6.value,
                          build_ele.FirstOpeningXPosit6.value, build_ele.FirstOpeningZPosit6.value, "FirstOpeningXPosit6", "FirstOpeningWidth6"]
        self.sec_open6 = [build_ele.SecondOpening6.value, build_ele.SecondOpeningWidth6.value, build_ele.SecondOpeningHeight6.value,
                          build_ele.SecondOpeningXPosit6.value, build_ele.SecondOpeningZPosit6.value, "SecondOpeningXPosit6", "SecondOpeningWidth6"]
        self.thi_open6 = [build_ele.ThirdOpening6.value, build_ele.ThirdOpeningWidth6.value, build_ele.ThirdOpeningHeight6.value,
                          build_ele.ThirdOpeningXPosit6.value, build_ele.ThirdOpeningZPosit6.value, "ThirdOpeningXPosit6", "ThirdOpeningWidth6"]
        self.fou_open6 = [build_ele.FourthOpening6.value, build_ele.FourthOpeningWidth6.value, build_ele.FourthOpeningHeight6.value,
                          build_ele.FourthOpeningXPosit6.value, build_ele.FourthOpeningZPosit6.value, "FourthOpeningXPosit6", "FourthOpeningWidth6"]
        self.fif_open6 = [build_ele.FifthOpening6.value, build_ele.FifthOpeningWidth6.value, build_ele.FifthOpeningHeight6.value,
                          build_ele.FifthOpeningXPosit6.value, build_ele.FifthOpeningZPosit6.value, "FifthOpeningXPosit6", "FifthOpeningWidth6"]
        self.six_open6 = [build_ele.SixthOpening6.value, build_ele.SixthOpeningWidth6.value, build_ele.SixthOpeningHeight6.value,
                          build_ele.SixthOpeningXPosit6.value, build_ele.SixthOpeningZPosit6.value, "SixthOpeningXPosit6", "SixthOpeningWidth6"]      
        self.sev_open6 = [build_ele.SeventhOpening6.value, build_ele.SeventhOpeningWidth6.value, build_ele.SeventhOpeningHeight6.value,
                          build_ele.SeventhOpeningXPosit6.value, build_ele.SeventhOpeningZPosit6.value, "SeventhOpeningXPosit6", "SeventhOpeningWidth6"]
        self.eig_open6 = [build_ele.EighthOpening6.value, build_ele.EighthOpeningWidth6.value, build_ele.EighthOpeningHeight6.value,
                          build_ele.EighthOpeningXPosit6.value, build_ele.EighthOpeningZPosit6.value, "EighthOpeningXPosit6", "EighthOpeningWidth6"]
        self.nin_open6 = [build_ele.NinthOpening6.value, build_ele.NinthOpeningWidth6.value, build_ele.NinthOpeningHeight6.value,
                          build_ele.NinthOpeningXPosit6.value, build_ele.NinthOpeningZPosit6.value, "NinthOpeningXPosit6", "NinthOpeningWidth6"]
        self.ten_open6 = [build_ele.TenthOpening6.value, build_ele.TenthOpeningWidth6.value, build_ele.TenthOpeningHeight6.value,
                          build_ele.TenthOpeningXPosit6.value, build_ele.TenthOpeningZPosit6.value, "TenthOpeningXPosit6", "TenthOpeningWidth6"]
        self.ele_open6 = [build_ele.EleventhOpening6.value, build_ele.EleventhOpeningWidth6.value, build_ele.EleventhOpeningHeight6.value,
                          build_ele.EleventhOpeningXPosit6.value, build_ele.EleventhOpeningZPosit6.value, "EleventhOpeningXPosit6", "EleventhOpeningWidth6"]
        self.twe_open6 = [build_ele.TwelfthOpening6.value, build_ele.TwelfthOpeningWidth6.value, build_ele.TwelfthOpeningHeight6.value,
                          build_ele.TwelfthOpeningXPosit6.value, build_ele.TwelfthOpeningZPosit6.value, "TwelfthOpeningXPosit6", "TwelfthOpeningWidth6"]

        self.fir_door6 = [build_ele.FirstDoor6.value, build_ele.FirstDoorWidth6.value, build_ele.FirstDoorHeight6.value,
                          build_ele.FirstDoorXPosit6.value, build_ele.FirstDoorZPosit6.value, "FirstDoorXPosit6", "FirstDoorWidth6"]
        self.sec_door6 = [build_ele.SecondDoor6.value, build_ele.SecondDoorWidth6.value, build_ele.SecondDoorHeight6.value,
                          build_ele.SecondDoorXPosit6.value, build_ele.SecondDoorZPosit6.value, "SecondDoorXPosit6", "SecondDoorWidth6"]
        self.thi_door6 = [build_ele.ThirdDoor6.value, build_ele.ThirdDoorWidth6.value, build_ele.ThirdDoorHeight6.value,
                          build_ele.ThirdDoorXPosit6.value, build_ele.ThirdDoorZPosit6.value, "ThirdDoorXPosit6", "ThirdDoorWidth6"]
        self.fou_door6 = [build_ele.FourthDoor6.value, build_ele.FourthDoorWidth6.value, build_ele.FourthDoorHeight6.value,
                          build_ele.FourthDoorXPosit6.value, build_ele.FourthDoorZPosit6.value, "FourthDoorXPosit6", "FourthDoorWidth6"]
        self.fif_door6 = [build_ele.FifthDoor6.value, build_ele.FifthDoorWidth6.value, build_ele.FifthDoorHeight6.value,
                          build_ele.FifthDoorXPosit6.value, build_ele.FifthDoorZPosit6.value, "FifthDoorXPosit6", "FifthDoorWidth6"]
        self.six_door6 = [build_ele.SixthDoor6.value, build_ele.SixthDoorWidth6.value, build_ele.SixthDoorHeight6.value,
                          build_ele.SixthDoorXPosit6.value, build_ele.SixthDoorZPosit6.value, "SixthDoorXPosit6", "SixthDoorWidth6"]      
        self.sev_door6 = [build_ele.SeventhDoor6.value, build_ele.SeventhDoorWidth6.value, build_ele.SeventhDoorHeight6.value,
                          build_ele.SeventhDoorXPosit6.value, build_ele.SeventhDoorZPosit6.value, "SeventhDoorXPosit6", "SeventhDoorWidth6"]
        self.eig_door6 = [build_ele.EighthDoor6.value, build_ele.EighthDoorWidth6.value, build_ele.EighthDoorHeight6.value,
                          build_ele.EighthDoorXPosit6.value, build_ele.EighthDoorZPosit6.value, "EighthDoorXPosit6", "EighthDoorWidth6"]
        self.nin_door6 = [build_ele.NinthDoor6.value, build_ele.NinthDoorWidth6.value, build_ele.NinthDoorHeight6.value,
                          build_ele.NinthDoorXPosit6.value, build_ele.NinthDoorZPosit6.value, "NinthDoorXPosit6", "NinthDoorWidth6"]
        self.ten_door6 = [build_ele.TenthDoor6.value, build_ele.TenthDoorWidth6.value, build_ele.TenthDoorHeight6.value,
                          build_ele.TenthDoorXPosit6.value, build_ele.TenthDoorZPosit6.value, "TenthDoorXPosit6", "TenthDoorWidth6"]
        self.ele_door6 = [build_ele.EleventhDoor6.value, build_ele.EleventhDoorWidth6.value, build_ele.EleventhDoorHeight6.value,
                          build_ele.EleventhDoorXPosit6.value, build_ele.EleventhDoorZPosit6.value, "EleventhDoorXPosit6", "EleventhDoorWidth6"]
        self.twe_door6 = [build_ele.TwelfthDoor6.value, build_ele.TwelfthDoorWidth6.value, build_ele.TwelfthDoorHeight6.value,
                          build_ele.TwelfthDoorXPosit6.value, build_ele.TwelfthDoorZPosit6.value, "TwelfthDoorXPosit6", "TwelfthDoorWidth6"]

        self.open6 = [self.fir_open6, self.sec_open6, self.thi_open6, self.fou_open6, self.fif_open6, self.six_open6, 
                     self.sev_open6, self.eig_open6, self.nin_open6, self.ten_open6, self.ele_open6, self.twe_open6]
        self.door6 = [self.fir_door6, self.sec_door6, self.thi_door6, self.fou_door6, self.fif_door6, self.six_door6, 
                     self.sev_door6, self.eig_door6, self.nin_door6, self.ten_door6, self.ele_door6, self.twe_door6]

        for open, door in zip(self.open6, self.door6):
            if door[0]:
                for idx in range(len(door)):
                    open[idx] = door[idx]

        self.insul6 = [build_ele.CreateInsulation6.value, build_ele.InsulWidth.value, build_ele.InsulHeight.value, 
                       build_ele.InsulThick.value, build_ele.InsulMinWidth.value]
        self.insul_type6 = build_ele.ThrLayPanel6.value
        self.hor_rib_thick6, self.ver_rib_thick6  = build_ele.HorRibThick6.value, build_ele.VerRibThick6.value
        self.open_hor_rib_thick6, self.open_ver_rib_thick6 = build_ele.OpenHorRibThick6.value, build_ele.OpenVerRibThick6.value

        #-----------------------------------------------------------SEVENTH WALL--------------------------------------------------------------------
        self.create_wall7 = build_ele.CreateWall7.value
        self.wall7 = [build_ele.WallLength7.value, build_ele.WallThick7.value, "WallLength7", build_ele.LeftEndOffset7.value, "LeftEndOffset7"]
        self.left_end7 = [build_ele.LeftEnd7.value, build_ele.LeftEndLength7.value, None]
        self.right_end7 = [build_ele.RightEnd7.value, build_ele.RightEndLength7.value, None]
        self.pylon_num7 = build_ele.PylonNum7.value 
        self.wall_offset7 = [build_ele.WallOffset7.value, "WallOffset7"]
        self.wall_inverse7 = build_ele.WallInverse7.value
        if not self.wall_inverse7:
            self.orient_params7 = [HandleDirection.x_dir, 0, self.wall_offset7[0], 0]
            self.orient_params7_1 = [HandleDirection.y_dir, self.wall7[3], self.wall7[1], 90]
        else:
            self.orient_params7 = [HandleDirection.x_dir, self.wall1[0], self.wall_offset7[0], 180]
            self.orient_params7_1 = [HandleDirection.y_dir, self.wall1[0] - self.wall7[3], -self.wall7[1], 90]
        
        self.fir_cent_pylon7 = [build_ele.FirstCentPylonLength7.value, build_ele.FirstCentPylonThick7.value, build_ele.FirstCentPylonPosit7.value, "FirstCentPylonPosit7"]
        self.sec_cent_pylon7 = [build_ele.SecondCentPylonLength7.value, build_ele.SecondCentPylonThick7.value, build_ele.SecondCentPylonPosit7.value, "SecondCentPylonPosit7"]
        self.thi_cent_pylon7 = [build_ele.ThirdCentPylonLength7.value, build_ele.ThirdCentPylonThick7.value, build_ele.ThirdCentPylonPosit7.value, "ThirdCentPylonPosit7"]

        self.fir_sect_wall7 = [build_ele.FirstSectWall7.value, build_ele.FirstSectWallLength7.value, build_ele.FirstSectWallPosit7.value, "FirstSectWallPosit7"]
        self.sec_sect_wall7 = [build_ele.SecondSectWall7.value, build_ele.SecondSectWallLength7.value, build_ele.SecondSectWallPosit7.value, "SecondSectWallPosit7"]
        self.thi_sect_wall7 = [build_ele.ThirdSectWall7.value, build_ele.ThirdSectWallLength7.value, build_ele.ThirdSectWallPosit7.value, "ThirdSectWallPosit7"]
        self.fou_sect_wall7 = [build_ele.FourthSectWall7.value, build_ele.FourthSectWallLength7.value, build_ele.FourthSectWallPosit7.value, "FourthSectWallPosit77"]
        self.fif_sect_wall7 = [build_ele.FifthSectWall7.value, build_ele.FifthSectWallLength7.value, build_ele.FifthSectWallPosit7.value, "FifthSectWallPosit7"]
        self.six_sect_wall7 = [build_ele.SixthSectWall7.value, build_ele.SixthSectWallLength7.value, build_ele.SixthSectWallPosit7.value, "SixthSectWallPosit7"]
        self.sev_sect_wall7 = [build_ele.SeventhSectWall7.value, build_ele.SeventhSectWallLength7.value, build_ele.SeventhSectWallPosit7.value, "SeventhSectWallPosit7"]
        self.eig_sect_wall7 = [build_ele.EighthSectWall7.value, build_ele.EighthSectWallLength7.value, build_ele.EighthSectWallPosit7.value, "EighthSectWallPosit7"]
       
        self.fir_open7 = [build_ele.FirstOpening7.value, build_ele.FirstOpeningWidth7.value, build_ele.FirstOpeningHeight7.value,
                          build_ele.FirstOpeningXPosit7.value, build_ele.FirstOpeningZPosit7.value, "FirstOpeningXPosit7", "FirstOpeningWidth7"]
        self.sec_open7 = [build_ele.SecondOpening7.value, build_ele.SecondOpeningWidth7.value, build_ele.SecondOpeningHeight7.value,
                          build_ele.SecondOpeningXPosit7.value, build_ele.SecondOpeningZPosit7.value, "SecondOpeningXPosit7", "SecondOpeningWidth7"]
        self.thi_open7 = [build_ele.ThirdOpening7.value, build_ele.ThirdOpeningWidth7.value, build_ele.ThirdOpeningHeight7.value,
                          build_ele.ThirdOpeningXPosit7.value, build_ele.ThirdOpeningZPosit7.value, "ThirdOpeningXPosit7", "ThirdOpeningWidth7"]
        self.fou_open7 = [build_ele.FourthOpening7.value, build_ele.FourthOpeningWidth7.value, build_ele.FourthOpeningHeight7.value,
                          build_ele.FourthOpeningXPosit7.value, build_ele.FourthOpeningZPosit7.value, "FourthOpeningXPosit7", "FourthOpeningWidth7"]
        self.fif_open7 = [build_ele.FifthOpening7.value, build_ele.FifthOpeningWidth7.value, build_ele.FifthOpeningHeight7.value,
                          build_ele.FifthOpeningXPosit7.value, build_ele.FifthOpeningZPosit7.value, "FifthOpeningXPosit7", "FifthOpeningWidth7"]
        self.six_open7 = [build_ele.SixthOpening7.value, build_ele.SixthOpeningWidth7.value, build_ele.SixthOpeningHeight7.value,
                          build_ele.SixthOpeningXPosit7.value, build_ele.SixthOpeningZPosit7.value, "SixthOpeningXPosit7", "SixthOpeningWidth7"]      
        self.sev_open7 = [build_ele.SeventhOpening7.value, build_ele.SeventhOpeningWidth7.value, build_ele.SeventhOpeningHeight7.value,
                          build_ele.SeventhOpeningXPosit7.value, build_ele.SeventhOpeningZPosit7.value, "SeventhOpeningXPosit7", "SeventhOpeningWidth7"]
        self.eig_open7 = [build_ele.EighthOpening7.value, build_ele.EighthOpeningWidth7.value, build_ele.EighthOpeningHeight7.value,
                          build_ele.EighthOpeningXPosit7.value, build_ele.EighthOpeningZPosit7.value, "EighthOpeningXPosit7", "EighthOpeningWidth7"]
        self.nin_open7 = [build_ele.NinthOpening7.value, build_ele.NinthOpeningWidth7.value, build_ele.NinthOpeningHeight7.value,
                          build_ele.NinthOpeningXPosit7.value, build_ele.NinthOpeningZPosit7.value, "NinthOpeningXPosit7", "NinthOpeningWidth7"]
        self.ten_open7 = [build_ele.TenthOpening7.value, build_ele.TenthOpeningWidth7.value, build_ele.TenthOpeningHeight7.value,
                          build_ele.TenthOpeningXPosit7.value, build_ele.TenthOpeningZPosit7.value, "TenthOpeningXPosit7", "TenthOpeningWidth7"]
        self.ele_open7 = [build_ele.EleventhOpening7.value, build_ele.EleventhOpeningWidth7.value, build_ele.EleventhOpeningHeight7.value,
                          build_ele.EleventhOpeningXPosit7.value, build_ele.EleventhOpeningZPosit7.value, "EleventhOpeningXPosit7", "EleventhOpeningWidth7"]
        self.twe_open7 = [build_ele.TwelfthOpening7.value, build_ele.TwelfthOpeningWidth7.value, build_ele.TwelfthOpeningHeight7.value,
                          build_ele.TwelfthOpeningXPosit7.value, build_ele.TwelfthOpeningZPosit7.value, "TwelfthOpeningXPosit7", "TwelfthOpeningWidth7"]

        self.fir_door7 = [build_ele.FirstDoor7.value, build_ele.FirstDoorWidth7.value, build_ele.FirstDoorHeight7.value,
                          build_ele.FirstDoorXPosit7.value, build_ele.FirstDoorZPosit7.value, "FirstDoorXPosit7", "FirstDoorWidth7"]
        self.sec_door7 = [build_ele.SecondDoor7.value, build_ele.SecondDoorWidth7.value, build_ele.SecondDoorHeight7.value,
                          build_ele.SecondDoorXPosit7.value, build_ele.SecondDoorZPosit7.value, "SecondDoorXPosit7", "SecondDoorWidth7"]
        self.thi_door7 = [build_ele.ThirdDoor7.value, build_ele.ThirdDoorWidth7.value, build_ele.ThirdDoorHeight7.value,
                          build_ele.ThirdDoorXPosit7.value, build_ele.ThirdDoorZPosit7.value, "ThirdDoorXPosit7", "ThirdDoorWidth7"]
        self.fou_door7 = [build_ele.FourthDoor7.value, build_ele.FourthDoorWidth7.value, build_ele.FourthDoorHeight7.value,
                          build_ele.FourthDoorXPosit7.value, build_ele.FourthDoorZPosit7.value, "FourthDoorXPosit7", "FourthDoorWidth7"]
        self.fif_door7 = [build_ele.FifthDoor7.value, build_ele.FifthDoorWidth7.value, build_ele.FifthDoorHeight7.value,
                          build_ele.FifthDoorXPosit7.value, build_ele.FifthDoorZPosit7.value, "FifthDoorXPosit7", "FifthDoorWidth7"]
        self.six_door7 = [build_ele.SixthDoor7.value, build_ele.SixthDoorWidth7.value, build_ele.SixthDoorHeight7.value,
                          build_ele.SixthDoorXPosit7.value, build_ele.SixthDoorZPosit7.value, "SixthDoorXPosit7", "SixthDoorWidth7"]      
        self.sev_door7 = [build_ele.SeventhDoor7.value, build_ele.SeventhDoorWidth7.value, build_ele.SeventhDoorHeight7.value,
                          build_ele.SeventhDoorXPosit7.value, build_ele.SeventhDoorZPosit7.value, "SeventhDoorXPosit7", "SeventhDoorWidth7"]
        self.eig_door7 = [build_ele.EighthDoor7.value, build_ele.EighthDoorWidth7.value, build_ele.EighthDoorHeight7.value,
                          build_ele.EighthDoorXPosit7.value, build_ele.EighthDoorZPosit7.value, "EighthDoorXPosit7", "EighthDoorWidth7"]
        self.nin_door7 = [build_ele.NinthDoor7.value, build_ele.NinthDoorWidth7.value, build_ele.NinthDoorHeight7.value,
                          build_ele.NinthDoorXPosit7.value, build_ele.NinthDoorZPosit7.value, "NinthDoorXPosit7", "NinthDoorWidth7"]
        self.ten_door7 = [build_ele.TenthDoor7.value, build_ele.TenthDoorWidth7.value, build_ele.TenthDoorHeight7.value,
                          build_ele.TenthDoorXPosit7.value, build_ele.TenthDoorZPosit7.value, "TenthDoorXPosit7", "TenthDoorWidth7"]
        self.ele_door7 = [build_ele.EleventhDoor7.value, build_ele.EleventhDoorWidth7.value, build_ele.EleventhDoorHeight7.value,
                          build_ele.EleventhDoorXPosit7.value, build_ele.EleventhDoorZPosit7.value, "EleventhDoorXPosit7", "EleventhDoorWidth7"]
        self.twe_door7 = [build_ele.TwelfthDoor7.value, build_ele.TwelfthDoorWidth7.value, build_ele.TwelfthDoorHeight7.value,
                          build_ele.TwelfthDoorXPosit7.value, build_ele.TwelfthDoorZPosit7.value, "TwelfthDoorXPosit7", "TwelfthDoorWidth7"]

        self.open7 = [self.fir_open7, self.sec_open7, self.thi_open7, self.fou_open7, self.fif_open7, self.six_open7, 
                     self.sev_open7, self.eig_open7, self.nin_open7, self.ten_open7, self.ele_open7, self.twe_open7]
        self.door7 = [self.fir_door7, self.sec_door7, self.thi_door7, self.fou_door7, self.fif_door7, self.six_door7, 
                     self.sev_door7, self.eig_door7, self.nin_door7, self.ten_door7, self.ele_door7, self.twe_door7]

        for open, door in zip(self.open7, self.door7):
            if door[0]:
                for idx in range(len(door)):
                    open[idx] = door[idx]

        self.insul7 = [build_ele.CreateInsulation7.value, build_ele.InsulWidth.value, build_ele.InsulHeight.value, 
                       build_ele.InsulThick.value, build_ele.InsulMinWidth.value]
        self.insul_type7 = build_ele.ThrLayPanel7.value
        self.hor_rib_thick7, self.ver_rib_thick7  = build_ele.HorRibThick7.value, build_ele.VerRibThick7.value
        self.open_hor_rib_thick7, self.open_ver_rib_thick7 = build_ele.OpenHorRibThick7.value, build_ele.OpenVerRibThick7.value

        #-----------------------------------------------------------EIGHTH WALL---------------------------------------------------------------------
        self.create_wall8 = build_ele.CreateWall8.value
        self.wall8 = [build_ele.WallLength8.value, build_ele.WallThick8.value, "WallLength8", build_ele.LeftEndOffset8.value, "LeftEndOffset8"]
        self.left_end8 = [build_ele.LeftEnd8.value, build_ele.LeftEndLength8.value, None]
        self.right_end8 = [build_ele.RightEnd8.value, build_ele.RightEndLength8.value, None]
        self.pylon_num8 = build_ele.PylonNum8.value 
        self.wall_offset8 = [build_ele.WallOffset8.value, "WallOffset8"]
        self.wall_inverse8 = build_ele.WallInverse8.value
        if not self.wall_inverse8:
            self.orient_params8 = [HandleDirection.y_dir, self.wall_offset8[0], self.wall2[0], 270]
            self.orient_params8_1 = [HandleDirection.x_dir, self.wall8[1], self.wall2[0] - self.wall8[3], 0]
        else:
            self.orient_params8 = [HandleDirection.y_dir, self.wall_offset8[0], 0, 90]
            self.orient_params8_1 = [HandleDirection.x_dir, -self.wall8[1], self.wall8[3], 0]
        
        self.fir_cent_pylon8 = [build_ele.FirstCentPylonLength8.value, build_ele.FirstCentPylonThick8.value, build_ele.FirstCentPylonPosit8.value, "FirstCentPylonPosit8"]
        self.sec_cent_pylon8 = [build_ele.SecondCentPylonLength8.value, build_ele.SecondCentPylonThick8.value, build_ele.SecondCentPylonPosit8.value, "SecondCentPylonPosit8"]
        self.thi_cent_pylon8 = [build_ele.ThirdCentPylonLength8.value, build_ele.ThirdCentPylonThick8.value, build_ele.ThirdCentPylonPosit8.value, "ThirdCentPylonPosit8"]

        self.fir_sect_wall8 = [build_ele.FirstSectWall8.value, build_ele.FirstSectWallLength8.value, build_ele.FirstSectWallPosit8.value, "FirstSectWallPosit8"]
        self.sec_sect_wall8 = [build_ele.SecondSectWall8.value, build_ele.SecondSectWallLength8.value, build_ele.SecondSectWallPosit8.value, "SecondSectWallPosit8"]
        self.thi_sect_wall8 = [build_ele.ThirdSectWall8.value, build_ele.ThirdSectWallLength8.value, build_ele.ThirdSectWallPosit8.value, "ThirdSectWallPosit8"]
        self.fou_sect_wall8 = [build_ele.FourthSectWall8.value, build_ele.FourthSectWallLength8.value, build_ele.FourthSectWallPosit8.value, "FourthSectWallPosit88"]
        self.fif_sect_wall8 = [build_ele.FifthSectWall8.value, build_ele.FifthSectWallLength8.value, build_ele.FifthSectWallPosit8.value, "FifthSectWallPosit8"]
        self.six_sect_wall8 = [build_ele.SixthSectWall8.value, build_ele.SixthSectWallLength8.value, build_ele.SixthSectWallPosit8.value, "SixthSectWallPosit8"]
        self.sev_sect_wall8 = [build_ele.SeventhSectWall8.value, build_ele.SeventhSectWallLength8.value, build_ele.SeventhSectWallPosit8.value, "SeventhSectWallPosit8"]
        self.eig_sect_wall8 = [build_ele.EighthSectWall8.value, build_ele.EighthSectWallLength8.value, build_ele.EighthSectWallPosit8.value, "EighthSectWallPosit8"]
       
        self.fir_open8 = [build_ele.FirstOpening8.value, build_ele.FirstOpeningWidth8.value, build_ele.FirstOpeningHeight8.value,
                          build_ele.FirstOpeningXPosit8.value, build_ele.FirstOpeningZPosit8.value, "FirstOpeningXPosit8", "FirstOpeningWidth8"]
        self.sec_open8 = [build_ele.SecondOpening8.value, build_ele.SecondOpeningWidth8.value, build_ele.SecondOpeningHeight8.value,
                          build_ele.SecondOpeningXPosit8.value, build_ele.SecondOpeningZPosit8.value, "SecondOpeningXPosit8", "SecondOpeningWidth8"]
        self.thi_open8 = [build_ele.ThirdOpening8.value, build_ele.ThirdOpeningWidth8.value, build_ele.ThirdOpeningHeight8.value,
                          build_ele.ThirdOpeningXPosit8.value, build_ele.ThirdOpeningZPosit8.value, "ThirdOpeningXPosit8", "ThirdOpeningWidth8"]
        self.fou_open8 = [build_ele.FourthOpening8.value, build_ele.FourthOpeningWidth8.value, build_ele.FourthOpeningHeight8.value,
                          build_ele.FourthOpeningXPosit8.value, build_ele.FourthOpeningZPosit8.value, "FourthOpeningXPosit8", "FourthOpeningWidth8"]
        self.fif_open8 = [build_ele.FifthOpening8.value, build_ele.FifthOpeningWidth8.value, build_ele.FifthOpeningHeight8.value,
                          build_ele.FifthOpeningXPosit8.value, build_ele.FifthOpeningZPosit8.value, "FifthOpeningXPosit8", "FifthOpeningWidth8"]
        self.six_open8 = [build_ele.SixthOpening8.value, build_ele.SixthOpeningWidth8.value, build_ele.SixthOpeningHeight8.value,
                          build_ele.SixthOpeningXPosit8.value, build_ele.SixthOpeningZPosit8.value, "SixthOpeningXPosit8", "SixthOpeningWidth8"]      
        self.sev_open8 = [build_ele.SeventhOpening8.value, build_ele.SeventhOpeningWidth8.value, build_ele.SeventhOpeningHeight8.value,
                          build_ele.SeventhOpeningXPosit8.value, build_ele.SeventhOpeningZPosit8.value, "SeventhOpeningXPosit8", "SeventhOpeningWidth8"]
        self.eig_open8 = [build_ele.EighthOpening8.value, build_ele.EighthOpeningWidth8.value, build_ele.EighthOpeningHeight8.value,
                          build_ele.EighthOpeningXPosit8.value, build_ele.EighthOpeningZPosit8.value, "EighthOpeningXPosit8", "EighthOpeningWidth8"]
        self.nin_open8 = [build_ele.NinthOpening8.value, build_ele.NinthOpeningWidth8.value, build_ele.NinthOpeningHeight8.value,
                          build_ele.NinthOpeningXPosit8.value, build_ele.NinthOpeningZPosit8.value, "NinthOpeningXPosit8", "NinthOpeningWidth8"]
        self.ten_open8 = [build_ele.TenthOpening8.value, build_ele.TenthOpeningWidth8.value, build_ele.TenthOpeningHeight8.value,
                          build_ele.TenthOpeningXPosit8.value, build_ele.TenthOpeningZPosit8.value, "TenthOpeningXPosit8", "TenthOpeningWidth8"]
        self.ele_open8 = [build_ele.EleventhOpening8.value, build_ele.EleventhOpeningWidth8.value, build_ele.EleventhOpeningHeight8.value,
                          build_ele.EleventhOpeningXPosit8.value, build_ele.EleventhOpeningZPosit8.value, "EleventhOpeningXPosit8", "EleventhOpeningWidth8"]
        self.twe_open8 = [build_ele.TwelfthOpening8.value, build_ele.TwelfthOpeningWidth8.value, build_ele.TwelfthOpeningHeight8.value,
                          build_ele.TwelfthOpeningXPosit8.value, build_ele.TwelfthOpeningZPosit8.value, "TwelfthOpeningXPosit8", "TwelfthOpeningWidth8"]

        self.fir_door8 = [build_ele.FirstDoor8.value, build_ele.FirstDoorWidth8.value, build_ele.FirstDoorHeight8.value,
                          build_ele.FirstDoorXPosit8.value, build_ele.FirstDoorZPosit8.value, "FirstDoorXPosit8", "FirstDoorWidth8"]
        self.sec_door8 = [build_ele.SecondDoor8.value, build_ele.SecondDoorWidth8.value, build_ele.SecondDoorHeight8.value,
                          build_ele.SecondDoorXPosit8.value, build_ele.SecondDoorZPosit8.value, "SecondDoorXPosit8", "SecondDoorWidth8"]
        self.thi_door8 = [build_ele.ThirdDoor8.value, build_ele.ThirdDoorWidth8.value, build_ele.ThirdDoorHeight8.value,
                          build_ele.ThirdDoorXPosit8.value, build_ele.ThirdDoorZPosit8.value, "ThirdDoorXPosit8", "ThirdDoorWidth8"]
        self.fou_door8 = [build_ele.FourthDoor8.value, build_ele.FourthDoorWidth8.value, build_ele.FourthDoorHeight8.value,
                          build_ele.FourthDoorXPosit8.value, build_ele.FourthDoorZPosit8.value, "FourthDoorXPosit8", "FourthDoorWidth8"]
        self.fif_door8 = [build_ele.FifthDoor8.value, build_ele.FifthDoorWidth8.value, build_ele.FifthDoorHeight8.value,
                          build_ele.FifthDoorXPosit8.value, build_ele.FifthDoorZPosit8.value, "FifthDoorXPosit8", "FifthDoorWidth8"]
        self.six_door8 = [build_ele.SixthDoor8.value, build_ele.SixthDoorWidth8.value, build_ele.SixthDoorHeight8.value,
                          build_ele.SixthDoorXPosit8.value, build_ele.SixthDoorZPosit8.value, "SixthDoorXPosit8", "SixthDoorWidth8"]      
        self.sev_door8 = [build_ele.SeventhDoor8.value, build_ele.SeventhDoorWidth8.value, build_ele.SeventhDoorHeight8.value,
                          build_ele.SeventhDoorXPosit8.value, build_ele.SeventhDoorZPosit8.value, "SeventhDoorXPosit8", "SeventhDoorWidth8"]
        self.eig_door8 = [build_ele.EighthDoor8.value, build_ele.EighthDoorWidth8.value, build_ele.EighthDoorHeight8.value,
                          build_ele.EighthDoorXPosit8.value, build_ele.EighthDoorZPosit8.value, "EighthDoorXPosit8", "EighthDoorWidth8"]
        self.nin_door8 = [build_ele.NinthDoor8.value, build_ele.NinthDoorWidth8.value, build_ele.NinthDoorHeight8.value,
                          build_ele.NinthDoorXPosit8.value, build_ele.NinthDoorZPosit8.value, "NinthDoorXPosit8", "NinthDoorWidth8"]
        self.ten_door8 = [build_ele.TenthDoor8.value, build_ele.TenthDoorWidth8.value, build_ele.TenthDoorHeight8.value,
                          build_ele.TenthDoorXPosit8.value, build_ele.TenthDoorZPosit8.value, "TenthDoorXPosit8", "TenthDoorWidth8"]
        self.ele_door8 = [build_ele.EleventhDoor8.value, build_ele.EleventhDoorWidth8.value, build_ele.EleventhDoorHeight8.value,
                          build_ele.EleventhDoorXPosit8.value, build_ele.EleventhDoorZPosit8.value, "EleventhDoorXPosit8", "EleventhDoorWidth8"]
        self.twe_door8 = [build_ele.TwelfthDoor8.value, build_ele.TwelfthDoorWidth8.value, build_ele.TwelfthDoorHeight8.value,
                          build_ele.TwelfthDoorXPosit8.value, build_ele.TwelfthDoorZPosit8.value, "TwelfthDoorXPosit8", "TwelfthDoorWidth8"]

        self.open8 = [self.fir_open8, self.sec_open8, self.thi_open8, self.fou_open8, self.fif_open8, self.six_open8, 
                     self.sev_open8, self.eig_open8, self.nin_open8, self.ten_open8, self.ele_open8, self.twe_open8]
        self.door8 = [self.fir_door8, self.sec_door8, self.thi_door8, self.fou_door8, self.fif_door8, self.six_door8, 
                     self.sev_door8, self.eig_door8, self.nin_door8, self.ten_door8, self.ele_door8, self.twe_door8]

        for open, door in zip(self.open8, self.door8):
            if door[0]:
                for idx in range(len(door)):
                    open[idx] = door[idx]

        self.insul8 = [build_ele.CreateInsulation8.value, build_ele.InsulWidth.value, build_ele.InsulHeight.value, 
                       build_ele.InsulThick.value, build_ele.InsulMinWidth.value]
        self.insul_type8 = build_ele.ThrLayPanel8.value
        self.hor_rib_thick8, self.ver_rib_thick8  = build_ele.HorRibThick8.value, build_ele.VerRibThick8.value
        self.open_hor_rib_thick8, self.open_ver_rib_thick8 = build_ele.OpenHorRibThick8.value, build_ele.OpenVerRibThick8.value

        #-----------------------------------------------------------NINHTH WALL---------------------------------------------------------------------
        self.create_wall9 = build_ele.CreateWall9.value
        self.wall9 = [build_ele.WallLength9.value, build_ele.WallThick9.value, "WallLength9", build_ele.LeftEndOffset9.value, "LeftEndOffset9"]
        self.left_end9 = [build_ele.LeftEnd9.value, build_ele.LeftEndLength9.value, None]
        self.right_end9 = [build_ele.RightEnd9.value, build_ele.RightEndLength9.value, None]
        self.pylon_num9 = build_ele.PylonNum9.value 
        self.wall_offset9 = [build_ele.WallOffset9.value, "WallOffset9"]
        self.wall_inverse9 = build_ele.WallInverse9.value
        if not self.wall_inverse9:
            self.orient_params9 = [HandleDirection.y_dir, self.wall_offset9[0], self.wall2[0], 270]
            self.orient_params9_1 = [HandleDirection.x_dir, self.wall9[1], self.wall2[0] - self.wall9[3], 0]
        else:
            self.orient_params9 = [HandleDirection.y_dir, self.wall_offset9[0], 0, 90]
            self.orient_params9_1 = [HandleDirection.x_dir, -self.wall9[1], self.wall9[3], 0]
        
        self.fir_cent_pylon9 = [build_ele.FirstCentPylonLength9.value, build_ele.FirstCentPylonThick9.value, build_ele.FirstCentPylonPosit9.value, "FirstCentPylonPosit9"]
        self.sec_cent_pylon9 = [build_ele.SecondCentPylonLength9.value, build_ele.SecondCentPylonThick9.value, build_ele.SecondCentPylonPosit9.value, "SecondCentPylonPosit9"]
        self.thi_cent_pylon9 = [build_ele.ThirdCentPylonLength9.value, build_ele.ThirdCentPylonThick9.value, build_ele.ThirdCentPylonPosit9.value, "ThirdCentPylonPosit9"]

        self.fir_sect_wall9 = [build_ele.FirstSectWall9.value, build_ele.FirstSectWallLength9.value, build_ele.FirstSectWallPosit9.value, "FirstSectWallPosit9"]
        self.sec_sect_wall9 = [build_ele.SecondSectWall9.value, build_ele.SecondSectWallLength9.value, build_ele.SecondSectWallPosit9.value, "SecondSectWallPosit9"]
        self.thi_sect_wall9 = [build_ele.ThirdSectWall9.value, build_ele.ThirdSectWallLength9.value, build_ele.ThirdSectWallPosit9.value, "ThirdSectWallPosit9"]
        self.fou_sect_wall9 = [build_ele.FourthSectWall9.value, build_ele.FourthSectWallLength9.value, build_ele.FourthSectWallPosit9.value, "FourthSectWallPosit99"]
        self.fif_sect_wall9 = [build_ele.FifthSectWall9.value, build_ele.FifthSectWallLength9.value, build_ele.FifthSectWallPosit9.value, "FifthSectWallPosit9"]
        self.six_sect_wall9 = [build_ele.SixthSectWall9.value, build_ele.SixthSectWallLength9.value, build_ele.SixthSectWallPosit9.value, "SixthSectWallPosit9"]
        self.sev_sect_wall9 = [build_ele.SeventhSectWall9.value, build_ele.SeventhSectWallLength9.value, build_ele.SeventhSectWallPosit9.value, "SeventhSectWallPosit9"]
        self.eig_sect_wall9 = [build_ele.EighthSectWall9.value, build_ele.EighthSectWallLength9.value, build_ele.EighthSectWallPosit9.value, "EighthSectWallPosit9"]
       
        self.fir_open9 = [build_ele.FirstOpening9.value, build_ele.FirstOpeningWidth9.value, build_ele.FirstOpeningHeight9.value,
                          build_ele.FirstOpeningXPosit9.value, build_ele.FirstOpeningZPosit9.value, "FirstOpeningXPosit9", "FirstOpeningWidth9"]
        self.sec_open9 = [build_ele.SecondOpening9.value, build_ele.SecondOpeningWidth9.value, build_ele.SecondOpeningHeight9.value,
                          build_ele.SecondOpeningXPosit9.value, build_ele.SecondOpeningZPosit9.value, "SecondOpeningXPosit9", "SecondOpeningWidth9"]
        self.thi_open9 = [build_ele.ThirdOpening9.value, build_ele.ThirdOpeningWidth9.value, build_ele.ThirdOpeningHeight9.value,
                          build_ele.ThirdOpeningXPosit9.value, build_ele.ThirdOpeningZPosit9.value, "ThirdOpeningXPosit9", "ThirdOpeningWidth9"]
        self.fou_open9 = [build_ele.FourthOpening9.value, build_ele.FourthOpeningWidth9.value, build_ele.FourthOpeningHeight9.value,
                          build_ele.FourthOpeningXPosit9.value, build_ele.FourthOpeningZPosit9.value, "FourthOpeningXPosit9", "FourthOpeningWidth9"]
        self.fif_open9 = [build_ele.FifthOpening9.value, build_ele.FifthOpeningWidth9.value, build_ele.FifthOpeningHeight9.value,
                          build_ele.FifthOpeningXPosit9.value, build_ele.FifthOpeningZPosit9.value, "FifthOpeningXPosit9", "FifthOpeningWidth9"]
        self.six_open9 = [build_ele.SixthOpening9.value, build_ele.SixthOpeningWidth9.value, build_ele.SixthOpeningHeight9.value,
                          build_ele.SixthOpeningXPosit9.value, build_ele.SixthOpeningZPosit9.value, "SixthOpeningXPosit9", "SixthOpeningWidth9"]      
        self.sev_open9 = [build_ele.SeventhOpening9.value, build_ele.SeventhOpeningWidth9.value, build_ele.SeventhOpeningHeight9.value,
                          build_ele.SeventhOpeningXPosit9.value, build_ele.SeventhOpeningZPosit9.value, "SeventhOpeningXPosit9", "SeventhOpeningWidth9"]
        self.eig_open9 = [build_ele.EighthOpening9.value, build_ele.EighthOpeningWidth9.value, build_ele.EighthOpeningHeight9.value,
                          build_ele.EighthOpeningXPosit9.value, build_ele.EighthOpeningZPosit9.value, "EighthOpeningXPosit9", "EighthOpeningWidth9"]
        self.nin_open9 = [build_ele.NinthOpening9.value, build_ele.NinthOpeningWidth9.value, build_ele.NinthOpeningHeight9.value,
                          build_ele.NinthOpeningXPosit9.value, build_ele.NinthOpeningZPosit9.value, "NinthOpeningXPosit9", "NinthOpeningWidth9"]
        self.ten_open9 = [build_ele.TenthOpening9.value, build_ele.TenthOpeningWidth9.value, build_ele.TenthOpeningHeight9.value,
                          build_ele.TenthOpeningXPosit9.value, build_ele.TenthOpeningZPosit9.value, "TenthOpeningXPosit9", "TenthOpeningWidth9"]
        self.ele_open9 = [build_ele.EleventhOpening9.value, build_ele.EleventhOpeningWidth9.value, build_ele.EleventhOpeningHeight9.value,
                          build_ele.EleventhOpeningXPosit9.value, build_ele.EleventhOpeningZPosit9.value, "EleventhOpeningXPosit9", "EleventhOpeningWidth9"]
        self.twe_open9 = [build_ele.TwelfthOpening9.value, build_ele.TwelfthOpeningWidth9.value, build_ele.TwelfthOpeningHeight9.value,
                          build_ele.TwelfthOpeningXPosit9.value, build_ele.TwelfthOpeningZPosit9.value, "TwelfthOpeningXPosit9", "TwelfthOpeningWidth9"]

        self.fir_door9 = [build_ele.FirstDoor9.value, build_ele.FirstDoorWidth9.value, build_ele.FirstDoorHeight9.value,
                          build_ele.FirstDoorXPosit9.value, build_ele.FirstDoorZPosit9.value, "FirstDoorXPosit9", "FirstDoorWidth9"]
        self.sec_door9 = [build_ele.SecondDoor9.value, build_ele.SecondDoorWidth9.value, build_ele.SecondDoorHeight9.value,
                          build_ele.SecondDoorXPosit9.value, build_ele.SecondDoorZPosit9.value, "SecondDoorXPosit9", "SecondDoorWidth9"]
        self.thi_door9 = [build_ele.ThirdDoor9.value, build_ele.ThirdDoorWidth9.value, build_ele.ThirdDoorHeight9.value,
                          build_ele.ThirdDoorXPosit9.value, build_ele.ThirdDoorZPosit9.value, "ThirdDoorXPosit9", "ThirdDoorWidth9"]
        self.fou_door9 = [build_ele.FourthDoor9.value, build_ele.FourthDoorWidth9.value, build_ele.FourthDoorHeight9.value,
                          build_ele.FourthDoorXPosit9.value, build_ele.FourthDoorZPosit9.value, "FourthDoorXPosit9", "FourthDoorWidth9"]
        self.fif_door9 = [build_ele.FifthDoor9.value, build_ele.FifthDoorWidth9.value, build_ele.FifthDoorHeight9.value,
                          build_ele.FifthDoorXPosit9.value, build_ele.FifthDoorZPosit9.value, "FifthDoorXPosit9", "FifthDoorWidth9"]
        self.six_door9 = [build_ele.SixthDoor9.value, build_ele.SixthDoorWidth9.value, build_ele.SixthDoorHeight9.value,
                          build_ele.SixthDoorXPosit9.value, build_ele.SixthDoorZPosit9.value, "SixthDoorXPosit9", "SixthDoorWidth9"]      
        self.sev_door9 = [build_ele.SeventhDoor9.value, build_ele.SeventhDoorWidth9.value, build_ele.SeventhDoorHeight9.value,
                          build_ele.SeventhDoorXPosit9.value, build_ele.SeventhDoorZPosit9.value, "SeventhDoorXPosit9", "SeventhDoorWidth9"]
        self.eig_door9 = [build_ele.EighthDoor9.value, build_ele.EighthDoorWidth9.value, build_ele.EighthDoorHeight9.value,
                          build_ele.EighthDoorXPosit9.value, build_ele.EighthDoorZPosit9.value, "EighthDoorXPosit9", "EighthDoorWidth9"]
        self.nin_door9 = [build_ele.NinthDoor9.value, build_ele.NinthDoorWidth9.value, build_ele.NinthDoorHeight9.value,
                          build_ele.NinthDoorXPosit9.value, build_ele.NinthDoorZPosit9.value, "NinthDoorXPosit9", "NinthDoorWidth9"]
        self.ten_door9 = [build_ele.TenthDoor9.value, build_ele.TenthDoorWidth9.value, build_ele.TenthDoorHeight9.value,
                          build_ele.TenthDoorXPosit9.value, build_ele.TenthDoorZPosit9.value, "TenthDoorXPosit9", "TenthDoorWidth9"]
        self.ele_door9 = [build_ele.EleventhDoor9.value, build_ele.EleventhDoorWidth9.value, build_ele.EleventhDoorHeight9.value,
                          build_ele.EleventhDoorXPosit9.value, build_ele.EleventhDoorZPosit9.value, "EleventhDoorXPosit9", "EleventhDoorWidth9"]
        self.twe_door9 = [build_ele.TwelfthDoor9.value, build_ele.TwelfthDoorWidth9.value, build_ele.TwelfthDoorHeight9.value,
                          build_ele.TwelfthDoorXPosit9.value, build_ele.TwelfthDoorZPosit9.value, "TwelfthDoorXPosit9", "TwelfthDoorWidth9"]

        self.open9 = [self.fir_open9, self.sec_open9, self.thi_open9, self.fou_open9, self.fif_open9, self.six_open9, 
                     self.sev_open9, self.eig_open9, self.nin_open9, self.ten_open9, self.ele_open9, self.twe_open9]
        self.door9 = [self.fir_door9, self.sec_door9, self.thi_door9, self.fou_door9, self.fif_door9, self.six_door9, 
                     self.sev_door9, self.eig_door9, self.nin_door9, self.ten_door9, self.ele_door9, self.twe_door9]

        for open, door in zip(self.open9, self.door9):
            if door[0]:
                for idx in range(len(door)):
                    open[idx] = door[idx]

        self.insul9 = [build_ele.CreateInsulation9.value, build_ele.InsulWidth.value, build_ele.InsulHeight.value, 
                       build_ele.InsulThick.value, build_ele.InsulMinWidth.value]
        self.insul_type9 = build_ele.ThrLayPanel9.value
        self.hor_rib_thick9, self.ver_rib_thick9  = build_ele.HorRibThick9.value, build_ele.VerRibThick9.value
        self.open_hor_rib_thick9, self.open_ver_rib_thick9 = build_ele.OpenHorRibThick9.value, build_ele.OpenVerRibThick9.value

        #-----------------------------------------------------------TENTH WALL---------------------------------------------------------------------
        self.create_wall10 = build_ele.CreateWall10.value
        self.wall10 = [build_ele.WallLength10.value, build_ele.WallThick10.value, "WallLength10", build_ele.LeftEndOffset10.value, "LeftEndOffset10"]
        self.left_end10 = [build_ele.LeftEnd10.value, build_ele.LeftEndLength10.value, None]
        self.right_end10 = [build_ele.RightEnd10.value, build_ele.RightEndLength10.value, None]
        self.pylon_num10 = build_ele.PylonNum10.value 
        self.wall_offset10 = [build_ele.WallOffset10.value, "WallOffset10"]
        self.wall_inverse10 = build_ele.WallInverse10.value
        if not self.wall_inverse10:
            self.orient_params10 = [HandleDirection.y_dir, self.wall_offset10[0], self.wall2[0], 270]
            self.orient_params10_1 = [HandleDirection.x_dir, self.wall10[1], self.wall2[0] - self.wall10[3], 0]
        else:
            self.orient_params10 = [HandleDirection.y_dir, self.wall_offset10[0], 0, 90]
            self.orient_params10_1 = [HandleDirection.x_dir, -self.wall10[1], self.wall10[3], 0]
        
        self.fir_cent_pylon10 = [build_ele.FirstCentPylonLength10.value, build_ele.FirstCentPylonThick10.value, build_ele.FirstCentPylonPosit10.value, "FirstCentPylonPosit10"]
        self.sec_cent_pylon10 = [build_ele.SecondCentPylonLength10.value, build_ele.SecondCentPylonThick10.value, build_ele.SecondCentPylonPosit10.value, "SecondCentPylonPosit10"]
        self.thi_cent_pylon10 = [build_ele.ThirdCentPylonLength10.value, build_ele.ThirdCentPylonThick10.value, build_ele.ThirdCentPylonPosit10.value, "ThirdCentPylonPosit10"]

        self.fir_sect_wall10 = [build_ele.FirstSectWall10.value, build_ele.FirstSectWallLength10.value, build_ele.FirstSectWallPosit10.value, "FirstSectWallPosit10"]
        self.sec_sect_wall10 = [build_ele.SecondSectWall10.value, build_ele.SecondSectWallLength10.value, build_ele.SecondSectWallPosit10.value, "SecondSectWallPosit10"]
        self.thi_sect_wall10 = [build_ele.ThirdSectWall10.value, build_ele.ThirdSectWallLength10.value, build_ele.ThirdSectWallPosit10.value, "ThirdSectWallPosit10"]
        self.fou_sect_wall10 = [build_ele.FourthSectWall10.value, build_ele.FourthSectWallLength10.value, build_ele.FourthSectWallPosit10.value, "FourthSectWallPosit1010"]
        self.fif_sect_wall10 = [build_ele.FifthSectWall10.value, build_ele.FifthSectWallLength10.value, build_ele.FifthSectWallPosit10.value, "FifthSectWallPosit10"]
        self.six_sect_wall10 = [build_ele.SixthSectWall10.value, build_ele.SixthSectWallLength10.value, build_ele.SixthSectWallPosit10.value, "SixthSectWallPosit10"]
        self.sev_sect_wall10 = [build_ele.SeventhSectWall10.value, build_ele.SeventhSectWallLength10.value, build_ele.SeventhSectWallPosit10.value, "SeventhSectWallPosit10"]
        self.eig_sect_wall10 = [build_ele.EighthSectWall10.value, build_ele.EighthSectWallLength10.value, build_ele.EighthSectWallPosit10.value, "EighthSectWallPosit10"]
       
        self.fir_open10 = [build_ele.FirstOpening10.value, build_ele.FirstOpeningWidth10.value, build_ele.FirstOpeningHeight10.value,
                          build_ele.FirstOpeningXPosit10.value, build_ele.FirstOpeningZPosit10.value, "FirstOpeningXPosit10", "FirstOpeningWidth10"]
        self.sec_open10 = [build_ele.SecondOpening10.value, build_ele.SecondOpeningWidth10.value, build_ele.SecondOpeningHeight10.value,
                          build_ele.SecondOpeningXPosit10.value, build_ele.SecondOpeningZPosit10.value, "SecondOpeningXPosit10", "SecondOpeningWidth10"]
        self.thi_open10 = [build_ele.ThirdOpening10.value, build_ele.ThirdOpeningWidth10.value, build_ele.ThirdOpeningHeight10.value,
                          build_ele.ThirdOpeningXPosit10.value, build_ele.ThirdOpeningZPosit10.value, "ThirdOpeningXPosit10", "ThirdOpeningWidth10"]
        self.fou_open10 = [build_ele.FourthOpening10.value, build_ele.FourthOpeningWidth10.value, build_ele.FourthOpeningHeight10.value,
                          build_ele.FourthOpeningXPosit10.value, build_ele.FourthOpeningZPosit10.value, "FourthOpeningXPosit10", "FourthOpeningWidth10"]
        self.fif_open10 = [build_ele.FifthOpening10.value, build_ele.FifthOpeningWidth10.value, build_ele.FifthOpeningHeight10.value,
                          build_ele.FifthOpeningXPosit10.value, build_ele.FifthOpeningZPosit10.value, "FifthOpeningXPosit10", "FifthOpeningWidth10"]
        self.six_open10 = [build_ele.SixthOpening10.value, build_ele.SixthOpeningWidth10.value, build_ele.SixthOpeningHeight10.value,
                          build_ele.SixthOpeningXPosit10.value, build_ele.SixthOpeningZPosit10.value, "SixthOpeningXPosit10", "SixthOpeningWidth10"]      
        self.sev_open10 = [build_ele.SeventhOpening10.value, build_ele.SeventhOpeningWidth10.value, build_ele.SeventhOpeningHeight10.value,
                          build_ele.SeventhOpeningXPosit10.value, build_ele.SeventhOpeningZPosit10.value, "SeventhOpeningXPosit10", "SeventhOpeningWidth10"]
        self.eig_open10 = [build_ele.EighthOpening10.value, build_ele.EighthOpeningWidth10.value, build_ele.EighthOpeningHeight10.value,
                          build_ele.EighthOpeningXPosit10.value, build_ele.EighthOpeningZPosit10.value, "EighthOpeningXPosit10", "EighthOpeningWidth10"]
        self.nin_open10 = [build_ele.NinthOpening10.value, build_ele.NinthOpeningWidth10.value, build_ele.NinthOpeningHeight10.value,
                          build_ele.NinthOpeningXPosit10.value, build_ele.NinthOpeningZPosit10.value, "NinthOpeningXPosit10", "NinthOpeningWidth10"]
        self.ten_open10 = [build_ele.TenthOpening10.value, build_ele.TenthOpeningWidth10.value, build_ele.TenthOpeningHeight10.value,
                          build_ele.TenthOpeningXPosit10.value, build_ele.TenthOpeningZPosit10.value, "TenthOpeningXPosit10", "TenthOpeningWidth10"]
        self.ele_open10 = [build_ele.EleventhOpening10.value, build_ele.EleventhOpeningWidth10.value, build_ele.EleventhOpeningHeight10.value,
                          build_ele.EleventhOpeningXPosit10.value, build_ele.EleventhOpeningZPosit10.value, "EleventhOpeningXPosit10", "EleventhOpeningWidth10"]
        self.twe_open10 = [build_ele.TwelfthOpening10.value, build_ele.TwelfthOpeningWidth10.value, build_ele.TwelfthOpeningHeight10.value,
                          build_ele.TwelfthOpeningXPosit10.value, build_ele.TwelfthOpeningZPosit10.value, "TwelfthOpeningXPosit10", "TwelfthOpeningWidth10"]

        self.fir_door10 = [build_ele.FirstDoor10.value, build_ele.FirstDoorWidth10.value, build_ele.FirstDoorHeight10.value,
                          build_ele.FirstDoorXPosit10.value, build_ele.FirstDoorZPosit10.value, "FirstDoorXPosit10", "FirstDoorWidth10"]
        self.sec_door10 = [build_ele.SecondDoor10.value, build_ele.SecondDoorWidth10.value, build_ele.SecondDoorHeight10.value,
                          build_ele.SecondDoorXPosit10.value, build_ele.SecondDoorZPosit10.value, "SecondDoorXPosit10", "SecondDoorWidth10"]
        self.thi_door10 = [build_ele.ThirdDoor10.value, build_ele.ThirdDoorWidth10.value, build_ele.ThirdDoorHeight10.value,
                          build_ele.ThirdDoorXPosit10.value, build_ele.ThirdDoorZPosit10.value, "ThirdDoorXPosit10", "ThirdDoorWidth10"]
        self.fou_door10 = [build_ele.FourthDoor10.value, build_ele.FourthDoorWidth10.value, build_ele.FourthDoorHeight10.value,
                          build_ele.FourthDoorXPosit10.value, build_ele.FourthDoorZPosit10.value, "FourthDoorXPosit10", "FourthDoorWidth10"]
        self.fif_door10 = [build_ele.FifthDoor10.value, build_ele.FifthDoorWidth10.value, build_ele.FifthDoorHeight10.value,
                          build_ele.FifthDoorXPosit10.value, build_ele.FifthDoorZPosit10.value, "FifthDoorXPosit10", "FifthDoorWidth10"]
        self.six_door10 = [build_ele.SixthDoor10.value, build_ele.SixthDoorWidth10.value, build_ele.SixthDoorHeight10.value,
                          build_ele.SixthDoorXPosit10.value, build_ele.SixthDoorZPosit10.value, "SixthDoorXPosit10", "SixthDoorWidth10"]      
        self.sev_door10 = [build_ele.SeventhDoor10.value, build_ele.SeventhDoorWidth10.value, build_ele.SeventhDoorHeight10.value,
                          build_ele.SeventhDoorXPosit10.value, build_ele.SeventhDoorZPosit10.value, "SeventhDoorXPosit10", "SeventhDoorWidth10"]
        self.eig_door10 = [build_ele.EighthDoor10.value, build_ele.EighthDoorWidth10.value, build_ele.EighthDoorHeight10.value,
                          build_ele.EighthDoorXPosit10.value, build_ele.EighthDoorZPosit10.value, "EighthDoorXPosit10", "EighthDoorWidth10"]
        self.nin_door10 = [build_ele.NinthDoor10.value, build_ele.NinthDoorWidth10.value, build_ele.NinthDoorHeight10.value,
                          build_ele.NinthDoorXPosit10.value, build_ele.NinthDoorZPosit10.value, "NinthDoorXPosit10", "NinthDoorWidth10"]
        self.ten_door10 = [build_ele.TenthDoor10.value, build_ele.TenthDoorWidth10.value, build_ele.TenthDoorHeight10.value,
                          build_ele.TenthDoorXPosit10.value, build_ele.TenthDoorZPosit10.value, "TenthDoorXPosit10", "TenthDoorWidth10"]
        self.ele_door10 = [build_ele.EleventhDoor10.value, build_ele.EleventhDoorWidth10.value, build_ele.EleventhDoorHeight10.value,
                          build_ele.EleventhDoorXPosit10.value, build_ele.EleventhDoorZPosit10.value, "EleventhDoorXPosit10", "EleventhDoorWidth10"]
        self.twe_door10 = [build_ele.TwelfthDoor10.value, build_ele.TwelfthDoorWidth10.value, build_ele.TwelfthDoorHeight10.value,
                          build_ele.TwelfthDoorXPosit10.value, build_ele.TwelfthDoorZPosit10.value, "TwelfthDoorXPosit10", "TwelfthDoorWidth10"]

        self.open10 = [self.fir_open10, self.sec_open10, self.thi_open10, self.fou_open10, self.fif_open10, self.six_open10, 
                     self.sev_open10, self.eig_open10, self.nin_open10, self.ten_open10, self.ele_open10, self.twe_open10]
        self.door10 = [self.fir_door10, self.sec_door10, self.thi_door10, self.fou_door10, self.fif_door10, self.six_door10, 
                     self.sev_door10, self.eig_door10, self.nin_door10, self.ten_door10, self.ele_door10, self.twe_door10]

        for open, door in zip(self.open10, self.door10):
            if door[0]:
                for idx in range(len(door)):
                    open[idx] = door[idx]

        self.insul10 = [build_ele.CreateInsulation10.value, build_ele.InsulWidth.value, build_ele.InsulHeight.value, 
                       build_ele.InsulThick.value, build_ele.InsulMinWidth.value]
        self.insul_type10 = build_ele.ThrLayPanel10.value
        self.hor_rib_thick10, self.ver_rib_thick10  = build_ele.HorRibThick10.value, build_ele.VerRibThick10.value
        self.open_hor_rib_thick10, self.open_ver_rib_thick10 = build_ele.OpenHorRibThick10.value, build_ele.OpenVerRibThick10.value

    def create_wall(self):
        #-----------------------------------------------------------CREATE FIRST WALL---------------------------------------------------------------
        if self.create_wall1:             
            wall1 = Create_Wall(self.build_ele, self.slab_thick, self.module_type, self.wall1, self.wall_offset, self.orient_params1, self.orient_params, self.left_end1, self.right_end1, 
                                self.pylon_num1, self.fir_cent_pylon1, self.sec_cent_pylon1, self.thi_cent_pylon1, self.fir_sect_wall1, self.sec_sect_wall1, self.thi_sect_wall1, 
                                self.fou_sect_wall1, self.fif_sect_wall1, self.six_sect_wall1, self.sev_sect_wall1, self.eig_sect_wall1, self.fir_open1, self.sec_open1, self.thi_open1, 
                                self.fou_open1, self.fif_open1, self.six_open1, self.sev_open1, self.eig_open1, self.nin_open1, self.ten_open1, self.ele_open1, self.twe_open1, self.insul1, 
                                self.hor_rib_thick1,  self.ver_rib_thick1, self.open_ver_rib_thick1, self.open_hor_rib_thick1, 100000, self.create_filling, self.pylon_thick_eq_wall_thick, self.insul_type1)
            if (self.pylon_num1 == "1"):
                wall1.create_wall_with_cent_pylon()
            elif (self.pylon_num1 == "2"):
                wall1.create_wall_with_two_cent_pylon()
            elif (self.pylon_num1 == "3"):
                wall1.create_wall_with_three_cent_pylon()
            else:
                wall1.create_wall()
            self.model_ele_list = wall1.model_ele_list
            self.fixture_elements = wall1.fixture_elements
            self.library_ele_list = wall1.library_ele_list
            if self.create_handle == True:
                self.handle_list = wall1.handle_list

            com_prop = AllplanBaseElements.CommonProperties()
            com_prop.GetGlobalProperties()
            line = AllplanGeo.Polyline3D()
            line += AllplanGeo.Point3D(0, 0, 0)
            line += AllplanGeo.Point3D(self.build_ele.ModuleLength.value, self.build_ele.ModuleWidth.value, 0)
            self.model_ele_list.append(AllplanBasisElements.ModelElement3D(com_prop, line))
       
        #-----------------------------------------------------------CREATE SECOND WALL--------------------------------------------------------------
        if self.create_wall2:             
            wall2 = Create_Wall(self.build_ele, self.slab_thick, self.module_type, self.wall2, self.wall_offset, self.orient_params2, self.orient_params, self.left_end2, self.right_end2, 
                                self.pylon_num2, self.fir_cent_pylon2, self.sec_cent_pylon2, self.thi_cent_pylon2, self.fir_sect_wall2, self.sec_sect_wall2, self.thi_sect_wall2, 
                                self.fou_sect_wall2, self.fif_sect_wall2, self.six_sect_wall2, self.sev_sect_wall2, self.eig_sect_wall2, self.fir_open2, self.sec_open2, self.thi_open2, 
                                self.fou_open2, self.fif_open2, self.six_open2, self.sev_open2, self.eig_open2, self.nin_open2, self.ten_open2, self.ele_open2, self.twe_open2, self.insul2, 
                                self.hor_rib_thick2, self.ver_rib_thick2, self.open_ver_rib_thick2, self.open_hor_rib_thick2, 200000, self.create_filling, self.pylon_thick_eq_wall_thick, self.insul_type2)
            if (self.pylon_num2 == "1"):
                wall2.create_wall_with_cent_pylon()
            elif (self.pylon_num2 == "2"):
                wall2.create_wall_with_two_cent_pylon()
            elif (self.pylon_num2 == "3"):
                wall2.create_wall_with_three_cent_pylon()
            else:
                wall2.create_wall()
            AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(self.wall1[0], 0, 0), 0, 0, 90, wall2.model_ele_list)
            AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(self.wall1[0], 0, 0), 0, 0, 90, wall2.fixture_elements)
            AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(self.wall1[0], 0, 0), 0, 0, 90, wall2.library_ele_list)
            if self.create_handle == True:
                self.handle_list.extend(wall2.handle_list)
            self.model_ele_list.extend(wall2.model_ele_list)
            self.fixture_elements.extend(wall2.fixture_elements)
            self.library_ele_list.extend(wall2.library_ele_list)

        #-----------------------------------------------------------CREATE THIRD WALL---------------------------------------------------------------
        if self.create_wall3:             
            wall3 = Create_Wall(self.build_ele, self.slab_thick, self.module_type, self.wall3, self.wall_offset, self.orient_params3, self.orient_params, self.left_end3, self.right_end3, 
                                self.pylon_num3, self.fir_cent_pylon3, self.sec_cent_pylon3, self.thi_cent_pylon3, self.fir_sect_wall3, self.sec_sect_wall3, self.thi_sect_wall3, 
                                self.fou_sect_wall3, self.fif_sect_wall3, self.six_sect_wall3, self.sev_sect_wall3, self.eig_sect_wall3, self.fir_open3, self.sec_open3, self.thi_open3, 
                                self.fou_open3, self.fif_open3, self.six_open3, self.sev_open3, self.eig_open3, self.nin_open3, self.ten_open3, self.ele_open3, self.twe_open3, self.insul3, 
                                self.hor_rib_thick3, self.ver_rib_thick3, self.open_ver_rib_thick3, self.open_hor_rib_thick3, 300000, self.create_filling, self.pylon_thick_eq_wall_thick, self.insul_type3)
            if (self.pylon_num3 == "1"):
                wall3.create_wall_with_cent_pylon()
            elif (self.pylon_num3 == "2"):
                wall3.create_wall_with_two_cent_pylon()
            elif (self.pylon_num3 == "3"):
                wall3.create_wall_with_three_cent_pylon()
            else:
                wall3.create_wall()
            AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(self.wall3[0], self.wall2[0], 0), 0, 0, 180, wall3.model_ele_list)
            AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(self.wall3[0], self.wall2[0], 0), 0, 0, 180, wall3.fixture_elements)
            AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(self.wall3[0], self.wall2[0], 0), 0, 0, 180, wall3.library_ele_list)
            self.model_ele_list.extend(wall3.model_ele_list)
            self.fixture_elements.extend(wall3.fixture_elements)
            self.library_ele_list.extend(wall3.library_ele_list)
            if self.create_handle == True:
                self.handle_list.extend(wall3.handle_list)

        #-----------------------------------------------------------CREATE FOURTH WALL--------------------------------------------------------------
        if self.create_wall4:             
            wall4 = Create_Wall(self.build_ele, self.slab_thick, self.module_type, self.wall4, self.wall_offset, self.orient_params4, self.orient_params, self.left_end4, self.right_end4, 
                                self.pylon_num4, self.fir_cent_pylon4, self.sec_cent_pylon4, self.thi_cent_pylon4, self.fir_sect_wall4, self.sec_sect_wall4, self.thi_sect_wall4, 
                                self.fou_sect_wall4, self.fif_sect_wall4, self.six_sect_wall4, self.sev_sect_wall4, self.eig_sect_wall4, self.fir_open4, self.sec_open4, self.thi_open4, 
                                self.fou_open4, self.fif_open4, self.six_open4, self.sev_open4, self.eig_open4, self.nin_open4, self.ten_open4, self.ele_open4, self.twe_open4, self.insul4, 
                                self.hor_rib_thick4, self.ver_rib_thick4, self.open_ver_rib_thick4, self.open_hor_rib_thick4, 400000, self.create_filling, self.pylon_thick_eq_wall_thick, self.insul_type4)
            if (self.pylon_num4 == "1"):
                wall4.create_wall_with_cent_pylon()
            elif (self.pylon_num4 == "2"):
                wall4.create_wall_with_two_cent_pylon()
            elif (self.pylon_num4 == "3"):
                wall4.create_wall_with_three_cent_pylon()
            else:
                wall4.create_wall()
            AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(0, self.wall4[0], 0), 0, 0, 270, wall4.model_ele_list)
            AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(0, self.wall4[0], 0), 0, 0, 270, wall4.fixture_elements)
            AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(0, self.wall4[0], 0), 0, 0, 270, wall4.library_ele_list)
            self.model_ele_list.extend(wall4.model_ele_list)
            self.fixture_elements.extend(wall4.fixture_elements)
            self.library_ele_list.extend(wall4.library_ele_list)
            if self.create_handle == True:
                self.handle_list.extend(wall4.handle_list)

        #-----------------------------------------------------------CREATE FIFTH WALL--------------------------------------------------------------
        if self.create_wall5:             
            wall5 = Create_Wall(self.build_ele, self.slab_thick, self.module_type, self.wall5, self.wall_offset5, self.orient_params5, self.orient_params5_1, self.left_end5, self.right_end5, 
                                self.pylon_num5, self.fir_cent_pylon5, self.sec_cent_pylon5, self.thi_cent_pylon5, self.fir_sect_wall5, self.sec_sect_wall5, self.thi_sect_wall5, 
                                self.fou_sect_wall5, self.fif_sect_wall5, self.six_sect_wall5, self.sev_sect_wall5, self.eig_sect_wall5, self.fir_open5, self.sec_open5, self.thi_open5, 
                                self.fou_open5, self.fif_open5, self.six_open5, self.sev_open5, self.eig_open5, self.nin_open5, self.ten_open5, self.ele_open5, self.twe_open5, self.insul5, 
                                self.hor_rib_thick5, self.ver_rib_thick5, self.open_ver_rib_thick5, self.open_hor_rib_thick5, 500000, self.create_filling, self.pylon_thick_eq_wall_thick, self.insul_type5)        
            if (self.pylon_num5 == "1"):
                wall5.create_wall_with_cent_pylon()
            elif (self.pylon_num5 == "2"):
                wall5.create_wall_with_two_cent_pylon()
            elif (self.pylon_num5 == "3"):
                wall5.create_wall_with_three_cent_pylon()
            else:
                wall5.create_wall()
            if not self.wall_inverse5:
                AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(0, self.wall_offset5[0], 0), 0, 0, 0, wall5.model_ele_list)
                AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(0, self.wall_offset5[0], 0), 0, 0, 0, wall5.fixture_elements)
                AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(0, self.wall_offset5[0], 0), 0, 0, 0, wall5.library_ele_list)
            else:
                AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(self.wall1[0], self.wall_offset5[0], 0), 0, 0, 180, wall5.model_ele_list)
                AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(self.wall1[0], self.wall_offset5[0], 0), 0, 0, 180, wall5.fixture_elements)
                AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(self.wall1[0], self.wall_offset5[0], 0), 0, 0, 180, wall5.library_ele_list)
            self.model_ele_list.extend(wall5.model_ele_list)
            self.fixture_elements.extend(wall5.fixture_elements)
            self.library_ele_list.extend(wall5.library_ele_list)
            if self.create_handle == True:
                self.handle_list.extend(wall5.handle_list)

        #-----------------------------------------------------------CREATE SIXTH WALL--------------------------------------------------------------
        if self.create_wall6:             
            wall6 = Create_Wall(self.build_ele, self.slab_thick, self.module_type, self.wall6, self.wall_offset6, self.orient_params6, self.orient_params6_1, self.left_end6, self.right_end6, 
                                self.pylon_num6, self.fir_cent_pylon6, self.sec_cent_pylon6, self.thi_cent_pylon6, self.fir_sect_wall6, self.sec_sect_wall6, self.thi_sect_wall6, 
                                self.fou_sect_wall6, self.fif_sect_wall6, self.six_sect_wall6, self.sev_sect_wall6, self.eig_sect_wall6, self.fir_open6, self.sec_open6, self.thi_open6, 
                                self.fou_open6, self.fif_open6, self.six_open6, self.sev_open6, self.eig_open6, self.nin_open6, self.ten_open6, self.ele_open6, self.twe_open6, self.insul6, 
                                self.hor_rib_thick6, self.ver_rib_thick6, self.open_ver_rib_thick6, self.open_hor_rib_thick6, 600000, self.create_filling, self.pylon_thick_eq_wall_thick, self.insul_type6)
            if (self.pylon_num6 == "1"):
                wall6.create_wall_with_cent_pylon()
            elif (self.pylon_num6 == "2"):
                wall6.create_wall_with_two_cent_pylon()
            elif (self.pylon_num6 == "3"):
                wall6.create_wall_with_three_cent_pylon()
            else:
                wall6.create_wall()
            if not self.wall_inverse6:
                AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(0, self.wall_offset6[0], 0), 0, 0, 0, wall6.model_ele_list)
                AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(0, self.wall_offset6[0], 0), 0, 0, 0, wall6.fixture_elements)
                AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(0, self.wall_offset6[0], 0), 0, 0, 0, wall6.library_ele_list)
            else:
                AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(self.wall1[0], self.wall_offset6[0], 0), 0, 0, 180, wall6.model_ele_list)
                AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(self.wall1[0], self.wall_offset6[0], 0), 0, 0, 180, wall6.fixture_elements)
                AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(self.wall1[0], self.wall_offset6[0], 0), 0, 0, 180, wall6.library_ele_list)
            self.model_ele_list.extend(wall6.model_ele_list)
            self.fixture_elements.extend(wall6.fixture_elements)
            self.library_ele_list.extend(wall6.library_ele_list)
            if self.create_handle == True:
                self.handle_list.extend(wall6.handle_list)

        #-----------------------------------------------------------CREATE SEVENTH WALL--------------------------------------------------------------
        if self.create_wall7:             
            wall7 = Create_Wall(self.build_ele, self.slab_thick, self.module_type, self.wall7, self.wall_offset7, self.orient_params7, self.orient_params7_1, self.left_end7, self.right_end7, 
                                self.pylon_num7, self.fir_cent_pylon7, self.sec_cent_pylon7, self.thi_cent_pylon7, self.fir_sect_wall7, self.sec_sect_wall7, self.thi_sect_wall7, 
                                self.fou_sect_wall7, self.fif_sect_wall7, self.six_sect_wall7, self.sev_sect_wall7, self.eig_sect_wall7, self.fir_open7, self.sec_open7, self.thi_open7, 
                                self.fou_open7, self.fif_open7, self.six_open7, self.sev_open7, self.eig_open7, self.nin_open7, self.ten_open7, self.ele_open7, self.twe_open7, self.insul7, 
                                self.hor_rib_thick7, self.ver_rib_thick7, self.open_ver_rib_thick7, self.open_hor_rib_thick7, 700000, self.create_filling, self.pylon_thick_eq_wall_thick, self.insul_type7)
            if (self.pylon_num7 == "1"):
                wall7.create_wall_with_cent_pylon()
            elif (self.pylon_num7 == "2"):
                wall7.create_wall_with_two_cent_pylon()
            elif (self.pylon_num7 == "3"):
                wall7.create_wall_with_three_cent_pylon()
            else:
                wall7.create_wall()
            if not self.wall_inverse7:
                AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(0, self.wall_offset7[0], 0), 0, 0, 0, wall7.model_ele_list)
                AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(0, self.wall_offset7[0], 0), 0, 0, 0, wall7.fixture_elements)
                AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(0, self.wall_offset7[0], 0), 0, 0, 0, wall7.library_ele_list)
            else:
                AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(self.wall1[0], self.wall_offset7[0], 0), 0, 0, 180, wall7.model_ele_list)
                AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(self.wall1[0], self.wall_offset7[0], 0), 0, 0, 180, wall7.fixture_elements)
                AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(self.wall1[0], self.wall_offset7[0], 0), 0, 0, 180, wall7.library_ele_list)
            self.model_ele_list.extend(wall7.model_ele_list)
            self.fixture_elements.extend(wall7.fixture_elements)
            self.library_ele_list.extend(wall7.library_ele_list)
            if self.create_handle == True:
                self.handle_list.extend(wall7.handle_list)

        #-----------------------------------------------------------CREATE EIGHTH WALL--------------------------------------------------------------
        if self.create_wall8:             
            wall8 = Create_Wall(self.build_ele, self.slab_thick, self.module_type, self.wall8, self.wall_offset8, self.orient_params8, self.orient_params8_1, self.left_end8, self.right_end8, 
                                self.pylon_num8, self.fir_cent_pylon8, self.sec_cent_pylon8, self.thi_cent_pylon8, self.fir_sect_wall8, self.sec_sect_wall8, self.thi_sect_wall8, 
                                self.fou_sect_wall8, self.fif_sect_wall8, self.six_sect_wall8, self.sev_sect_wall8, self.eig_sect_wall8, self.fir_open8, self.sec_open8, self.thi_open8, 
                                self.fou_open8, self.fif_open8, self.six_open8, self.sev_open8, self.eig_open8, self.nin_open8, self.ten_open8, self.ele_open8, self.twe_open8, self.insul8, 
                                self.hor_rib_thick8, self.ver_rib_thick8, self.open_ver_rib_thick8, self.open_hor_rib_thick8, 800000, self.create_filling, self.pylon_thick_eq_wall_thick, self.insul_type8)
            if (self.pylon_num8 == "1"):
                wall8.create_wall_with_cent_pylon()
            elif (self.pylon_num8 == "2"):
                wall8.create_wall_with_two_cent_pylon()
            elif (self.pylon_num8 == "3"):
                wall8.create_wall_with_three_cent_pylon()
            else:
                wall8.create_wall()
            if not self.wall_inverse8:
                AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(self.wall_offset8[0], self.wall2[0], 0), 0, 0, 270, wall8.model_ele_list)
                AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(self.wall_offset8[0], self.wall2[0], 0), 0, 0, 270, wall8.fixture_elements)
                AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(self.wall_offset8[0], self.wall2[0], 0), 0, 0, 270, wall8.library_ele_list)
            else:
                AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(self.wall_offset8[0], 0, 0), 0, 0, 90, wall8.model_ele_list)
                AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(self.wall_offset8[0], 0, 0), 0, 0, 90, wall8.fixture_elements)
                AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(self.wall_offset8[0], 0, 0), 0, 0, 90, wall8.library_ele_list)
            self.model_ele_list.extend(wall8.model_ele_list)
            self.fixture_elements.extend(wall8.fixture_elements)
            self.library_ele_list.extend(wall8.library_ele_list)
            if self.create_handle == True:
                self.handle_list.extend(wall8.handle_list)

        #-----------------------------------------------------------CREATE NINTH WALL--------------------------------------------------------------
        if self.create_wall9:             
            wall9 = Create_Wall(self.build_ele, self.slab_thick, self.module_type, self.wall9, self.wall_offset9, self.orient_params9, self.orient_params9_1, self.left_end9, self.right_end9, 
                                self.pylon_num9, self.fir_cent_pylon9, self.sec_cent_pylon9, self.thi_cent_pylon9, self.fir_sect_wall9, self.sec_sect_wall9, self.thi_sect_wall9, 
                                self.fou_sect_wall9, self.fif_sect_wall9, self.six_sect_wall9, self.sev_sect_wall9, self.eig_sect_wall9, self.fir_open9, self.sec_open9, self.thi_open9, 
                                self.fou_open9, self.fif_open9, self.six_open9, self.sev_open9, self.eig_open9, self.nin_open9, self.ten_open9, self.ele_open9, self.twe_open9, self.insul9, 
                                self.hor_rib_thick9, self.ver_rib_thick9, self.open_ver_rib_thick9, self.open_hor_rib_thick9, 900000, self.create_filling, self.pylon_thick_eq_wall_thick, self.insul_type9)
            if (self.pylon_num9 == "1"):
                wall9.create_wall_with_cent_pylon()
            elif (self.pylon_num9 == "2"):
                wall9.create_wall_with_two_cent_pylon()
            elif (self.pylon_num9 == "3"):
                wall9.create_wall_with_three_cent_pylon()
            else:
                wall9.create_wall()
            if not self.wall_inverse9:
                AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(self.wall_offset9[0], self.wall2[0], 0), 0, 0, 270, wall9.model_ele_list)
                AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(self.wall_offset9[0], self.wall2[0], 0), 0, 0, 270, wall9.fixture_elements)
                AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(self.wall_offset9[0], self.wall2[0], 0), 0, 0, 270, wall9.library_ele_list)
            else:
                AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(self.wall_offset9[0], 0, 0), 0, 0, 90, wall9.model_ele_list)
                AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(self.wall_offset9[0], 0, 0), 0, 0, 90, wall9.fixture_elements)
                AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(self.wall_offset9[0], 0, 0), 0, 0, 90, wall9.library_ele_list)
            self.model_ele_list.extend(wall9.model_ele_list)
            self.fixture_elements.extend(wall9.fixture_elements)
            self.library_ele_list.extend(wall9.library_ele_list)
            if self.create_handle == True:
                self.handle_list.extend(wall9.handle_list)

        #-----------------------------------------------------------CREATE TENTH WALL--------------------------------------------------------------
        if self.create_wall10:             
            wall10 = Create_Wall(self.build_ele, self.slab_thick, self.module_type, self.wall10, self.wall_offset10, self.orient_params10, self.orient_params10_1, self.left_end10, self.right_end10, 
                                self.pylon_num10, self.fir_cent_pylon10, self.sec_cent_pylon10, self.thi_cent_pylon10, self.fir_sect_wall10, self.sec_sect_wall10, self.thi_sect_wall10, 
                                self.fou_sect_wall10, self.fif_sect_wall10, self.six_sect_wall10, self.sev_sect_wall10, self.eig_sect_wall10, self.fir_open10, self.sec_open10, self.thi_open10, 
                                self.fou_open10, self.fif_open10, self.six_open10, self.sev_open10, self.eig_open10, self.nin_open10, self.ten_open10, self.ele_open10, self.twe_open10, self.insul10, 
                                self.hor_rib_thick10, self.ver_rib_thick10, self.open_ver_rib_thick10, self.open_hor_rib_thick10, 1000000, self.create_filling, self.pylon_thick_eq_wall_thick, self.insul_type10)
            if (self.pylon_num10 == "1"):
                wall10.create_wall_with_cent_pylon()
            elif (self.pylon_num10 == "2"):
                wall10.create_wall_with_two_cent_pylon()
            elif (self.pylon_num10 == "3"):
                wall10.create_wall_with_three_cent_pylon()
            else:
                wall10.create_wall()
            if not self.wall_inverse10:
                AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(self.wall_offset10[0], self.wall2[0], 0), 0, 0, 270, wall10.model_ele_list)
                AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(self.wall_offset10[0], self.wall2[0], 0), 0, 0, 270, wall10.fixture_elements)
                AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(self.wall_offset10[0], self.wall2[0], 0), 0, 0, 270, wall10.library_ele_list)
            else:
                AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(self.wall_offset10[0], 0, 0), 0, 0, 90, wall10.model_ele_list)
                AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(self.wall_offset10[0], 0, 0), 0, 0, 90, wall10.fixture_elements)
                AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(self.wall_offset10[0], 0, 0), 0, 0, 90, wall10.library_ele_list)
            self.model_ele_list.extend(wall10.model_ele_list)
            self.fixture_elements.extend(wall10.fixture_elements)
            self.library_ele_list.extend(wall10.library_ele_list)
            if self.create_handle == True:
                self.handle_list.extend(wall10.handle_list)

        if self.python_part:
            self.create_python_part(self.build_ele)
        else:
            self.model_ele_list.extend(self.fixture_elements)

    def create_python_part(self, build_ele):

        views = [View2D3D (self.model_ele_list)]
        pythonpart = PythonPart("Module", parameter_list = self.build_ele.get_params_list(), hash_value = self.build_ele.get_hash(),
                                python_file = self.build_ele.pyp_file_name, views = views, fixture_elements = self.fixture_elements,
                                library_elements = self.library_ele_list)
        #library_elements = self.library_ele_list
        self.model_ele_list = pythonpart.create()
            

class Create_Wall():
    def __init__(self, build_ele, slab_thick, module_type, wall, wall_offset, orient_params, orient_params1, left_end, right_end, pylon_num, fir_cent_pylon, 
                 sec_cent_pylon, thi_cent_pylon, fir_sect_wall, sec_sect_wall, thi_sect_wall, fou_sect_wall, fif_sect_wall, six_sect_wall, sev_sect_wall, 
                 eig_sect_wall, fir_open, sec_open, thi_open, fou_open, fif_open, six_open, sev_open, eig_open, nin_open, ten_open, ele_open, twe_open, 
                 insul, hor_rib_thick, ver_rib_thick, open_ver_rib_thick, open_hor_rib_thick, num, create_filling, pylon_thick_eq_wall_thick, insul_type):

        self.com_prop = AllplanBaseElements.CommonProperties()
        self.com_prop.GetGlobalProperties()
        self.com_prop.ColorByLayer = False
        self.com_prop.Layer = 3984
        self.com_prop.Pen = 1
        self.com_prop.Color = 1
        self.com_prop.Stroke = 1

        self.slab_thick = slab_thick
        self.module_type = module_type
        self.create_filling = create_filling
        self.pylon_thick_eq_wall_thick = pylon_thick_eq_wall_thick
        self.num = num
        
        self.floor_height = build_ele.FloorHeight.value
        self.wall_height = self.floor_height - 10
        self.rib_wall_height = self.wall_height - 300 - self.slab_thick

        self.wall = [wall[0], wall[1], wall[2], wall[3], wall[4]]
        self.wall_offset = [wall_offset[0], wall_offset[1]]
        self.left_end = [left_end[0], left_end[1], left_end[2]]
        self.right_end = [right_end[0], right_end[1], right_end[2]]
        self.pylon_num = pylon_num

        self.orient_params = [orient_params[0], orient_params[1], orient_params[2], orient_params[3]]
        self.orient_params1 = [orient_params1[0], orient_params1[1], orient_params1[2], orient_params1[3]]
        
        self.fir_cent_pylon = [fir_cent_pylon[0], fir_cent_pylon[1], fir_cent_pylon[2], fir_cent_pylon[3]]
        self.sec_cent_pylon = [sec_cent_pylon[0], sec_cent_pylon[1], sec_cent_pylon[2], sec_cent_pylon[3]]
        self.thi_cent_pylon = [thi_cent_pylon[0], thi_cent_pylon[1], thi_cent_pylon[2], thi_cent_pylon[3]]
        if self.pylon_thick_eq_wall_thick:
            self.fir_cent_pylon = [fir_cent_pylon[0], self.wall[1], fir_cent_pylon[2], fir_cent_pylon[3]]
            self.sec_cent_pylon = [sec_cent_pylon[0], self.wall[1], sec_cent_pylon[2], sec_cent_pylon[3]]
            self.thi_cent_pylon = [thi_cent_pylon[0], self.wall[1], thi_cent_pylon[2], thi_cent_pylon[3]]

        self.fir_sect_wall = [fir_sect_wall[0], fir_sect_wall[1], fir_sect_wall[2], fir_sect_wall[3]]
        self.sec_sect_wall = [sec_sect_wall[0], sec_sect_wall[1], sec_sect_wall[2], sec_sect_wall[3]]
        self.thi_sect_wall = [thi_sect_wall[0], thi_sect_wall[1], thi_sect_wall[2], thi_sect_wall[3]]
        self.fou_sect_wall = [fou_sect_wall[0], fou_sect_wall[1], fou_sect_wall[2], fou_sect_wall[3]]
        self.fif_sect_wall = [fif_sect_wall[0], fif_sect_wall[1], fif_sect_wall[2], fif_sect_wall[3]]
        self.six_sect_wall = [six_sect_wall[0], six_sect_wall[1], six_sect_wall[2], six_sect_wall[3]]
        self.sev_sect_wall = [sev_sect_wall[0], sev_sect_wall[1], sev_sect_wall[2], sev_sect_wall[3]]
        self.eig_sect_wall = [eig_sect_wall[0], eig_sect_wall[1], eig_sect_wall[2], eig_sect_wall[3]]

        self.fir_open = [fir_open[0], fir_open[1], fir_open[2], fir_open[3], fir_open[4] + self.slab_thick, fir_open[5], fir_open[6], 1] 
        self.sec_open = [sec_open[0], sec_open[1], sec_open[2], sec_open[3], sec_open[4] + self.slab_thick, sec_open[5], sec_open[6], 2]
        self.thi_open = [thi_open[0], thi_open[1], thi_open[2], thi_open[3], thi_open[4] + self.slab_thick, thi_open[5], thi_open[6], 3]
        self.fou_open = [fou_open[0], fou_open[1], fou_open[2], fou_open[3], fou_open[4] + self.slab_thick, fou_open[5], fou_open[6], 4]
        self.fif_open = [fif_open[0], fif_open[1], fif_open[2], fif_open[3], fif_open[4] + self.slab_thick, fif_open[5], fif_open[6], 5]
        self.six_open = [six_open[0], six_open[1], six_open[2], six_open[3], six_open[4] + self.slab_thick, six_open[5], six_open[6], 6]
        self.sev_open = [sev_open[0], sev_open[1], sev_open[2], sev_open[3], sev_open[4] + self.slab_thick, sev_open[5], sev_open[6], 7] 
        self.eig_open = [eig_open[0], eig_open[1], eig_open[2], eig_open[3], eig_open[4] + self.slab_thick, eig_open[5], eig_open[6], 8]
        self.nin_open = [nin_open[0], nin_open[1], nin_open[2], nin_open[3], nin_open[4] + self.slab_thick, nin_open[5], nin_open[6], 9]
        self.ten_open = [ten_open[0], ten_open[1], ten_open[2], ten_open[3], ten_open[4] + self.slab_thick, ten_open[5], ten_open[6], 10]
        self.ele_open = [ele_open[0], ele_open[1], ele_open[2], ele_open[3], ele_open[4] + self.slab_thick, ele_open[5], ele_open[6], 11]
        self.twe_open = [twe_open[0], twe_open[1], twe_open[2], twe_open[3], twe_open[4] + self.slab_thick, twe_open[5], twe_open[6], 12]

        self.insul = [insul[0], insul[1], insul[2], insul[3], insul[4]]
        self.insul_type = insul_type

        self.hor_rib_thick = hor_rib_thick
        self.ver_rib_thick = ver_rib_thick
        self.open_hor_rib_thick = open_hor_rib_thick
        self.open_ver_rib_thick = open_ver_rib_thick

        self.start_point = 0
        self.middle_point = self.fir_cent_pylon[2]
        self.end_point = 0

        self.model_ele_list = []
        self.fixture_elements = []
        self.library_ele_list = []
        self.handle_list = []
        
        self.wall_orient = None
     
    def create_wall(self): 
        wall = AllplanGeo.Polyhedron3D.CreateCuboid(self.wall[0], self.wall[1], self.wall_height)    
        wall = self.create_left_end(wall)
        wall = self.create_right_end(wall)
        self.create_opening(self.fir_open, self.sec_open, self.thi_open, int(self.num/1000))
        if self.insul[0] or self.create_filling:
            self.create_insulation(self.fir_open, self.sec_open, self.thi_open, self.fir_sect_wall, self.sec_sect_wall, self.wall[0], self.start_point, self.end_point, 0, self.insul_type, self.num)
        if not self.wall_offset[0]:
            self.create_handle(self.wall[0], self.wall[2], self.orient_params)
        else:
            wall = AllplanGeo.Move(wall, AllplanGeo.Vector3D(self.wall[3], 0, 0))
            self.create_handle(self.wall_offset[0], self.wall_offset[1], self.orient_params1)
            self.create_handle(self.wall[3], self.wall[4], self.orient_params)
            self.create_handle(self.wall[0] + self.wall[3], self.wall[2], self.orient_params, self.wall[3])
        self.model_ele_list.append(AllplanBasisElements.ModelElement3D(self.com_prop, wall))

    def create_wall_with_cent_pylon(self):
        wall_list = []
        wall_list.append(AllplanGeo.Polyhedron3D.CreateCuboid(self.fir_cent_pylon[2], self.wall[1], self.wall_height))
        wall_list.append(AllplanGeo.Polyhedron3D.CreateCuboid(self.wall[0] - self.fir_cent_pylon[2], self.wall[1], self.wall_height))
        wall_list[1] = AllplanGeo.Move(wall_list[1], AllplanGeo.Vector3D(self.fir_cent_pylon[2], 0, 0))
        wall_list[0] = self.create_left_end(wall_list[0])
        wall_list[1] = self.create_right_end(wall_list[1])
        self.create_opening(self.fir_open, self.sec_open, self.thi_open, int(self.num/1000))
        self.create_opening(self.fou_open, self.fif_open, self.six_open, int(self.num/1000))
        if self.insul[0] or self.create_filling:        
            self.create_insulation(self.fir_open, self.sec_open, self.thi_open, self.fir_sect_wall, self.sec_sect_wall, self.fir_cent_pylon[2], self.start_point, 0, 0, self.insul_type, self.num)
            self.create_insulation(self.fou_open, self.fif_open, self.six_open, self.thi_sect_wall, self.fou_sect_wall, self.wall[0] - self.fir_cent_pylon[2], self.fir_cent_pylon[0], self.end_point, self.fir_cent_pylon[2], self.insul_type, self.num+25000) 
        if not self.wall_offset[0]:
            self.create_handle(self.wall[0], self.wall[2], self.orient_params)
        else:
            wall_list[0] = AllplanGeo.Move(wall_list[0], AllplanGeo.Vector3D(self.wall[3], 0, 0))
            wall_list[1] = AllplanGeo.Move(wall_list[1], AllplanGeo.Vector3D(self.wall[3], 0, 0))
            self.create_handle(self.wall_offset[0], self.wall_offset[1], self.orient_params1)
            self.create_handle(self.wall[3], self.wall[4], self.orient_params)
            self.create_handle(self.wall[0] + self.wall[3], self.wall[2], self.orient_params, self.wall[3])
        wall = self.create_central_pylon(wall_list, self.fir_cent_pylon)
        self.model_ele_list.append(AllplanBasisElements.ModelElement3D(self.com_prop, wall))

    def create_wall_with_two_cent_pylon(self):           
        wall_list = []
        wall_list.append(AllplanGeo.Polyhedron3D.CreateCuboid(self.fir_cent_pylon[2], self.wall[1], self.wall_height))
        wall_list.append(AllplanGeo.Polyhedron3D.CreateCuboid(self.sec_cent_pylon[2] - self.fir_cent_pylon[2], self.wall[1], self.wall_height))
        wall_list.append(AllplanGeo.Polyhedron3D.CreateCuboid(self.wall[0] - self.sec_cent_pylon[2], self.wall[1], self.wall_height))
        wall_list[1] = AllplanGeo.Move(wall_list[1], AllplanGeo.Vector3D(self.fir_cent_pylon[2], 0, 0))
        wall_list[2] = AllplanGeo.Move(wall_list[2], AllplanGeo.Vector3D(self.sec_cent_pylon[2], 0, 0))
        wall_list[0] = self.create_left_end(wall_list[0])
        wall_list[2] = self.create_right_end(wall_list[2])
        self.create_opening(self.fir_open, self.sec_open, self.thi_open, int(self.num/1000))
        self.create_opening(self.fou_open, self.fif_open, self.six_open, int(self.num/1000))
        self.create_opening(self.sev_open, self.eig_open, self.nin_open, int(self.num/1000))
        if self.insul[0] or self.create_filling:
            self.create_insulation(self.fir_open, self.sec_open, self.thi_open, self.fir_sect_wall, self.sec_sect_wall, self.fir_cent_pylon[2], self.start_point, 0, 0, self.insul_type, self.num)
            self.create_insulation(self.fou_open, self.fif_open, self.six_open, self.thi_sect_wall, self.fou_sect_wall, self.sec_cent_pylon[2] - self.fir_cent_pylon[2], self.fir_cent_pylon[0], 0, self.fir_cent_pylon[2], self.insul_type, self.num+25000)
            self.create_insulation(self.sev_open, self.eig_open, self.nin_open, self.fif_sect_wall, self.six_sect_wall, self.wall[0] - self.sec_cent_pylon[2], self.sec_cent_pylon[0], self.end_point, self.sec_cent_pylon[2], self.insul_type, self.num+50000)
        if not self.wall_offset[0]:
            self.create_handle(self.wall[0], self.wall[2], self.orient_params)
        else:
            wall_list[0] = AllplanGeo.Move(wall_list[0], AllplanGeo.Vector3D(self.wall[3], 0, 0))
            wall_list[1] = AllplanGeo.Move(wall_list[1], AllplanGeo.Vector3D(self.wall[3], 0, 0))
            wall_list[2] = AllplanGeo.Move(wall_list[2], AllplanGeo.Vector3D(self.wall[3], 0, 0))
            self.create_handle(self.wall_offset[0], self.wall_offset[1], self.orient_params1)
            self.create_handle(self.wall[3], self.wall[4], self.orient_params)
            self.create_handle(self.wall[0] + self.wall[3], self.wall[2], self.orient_params, self.wall[3])
        wall = self.create_central_pylon(wall_list[0:2], self.fir_cent_pylon)
        wall = self.create_central_pylon([wall, wall_list[2]], self.sec_cent_pylon)
        self.model_ele_list.append(AllplanBasisElements.ModelElement3D(self.com_prop, wall))

    def create_wall_with_three_cent_pylon(self):           
        wall_list = []
        wall_list.append(AllplanGeo.Polyhedron3D.CreateCuboid(self.fir_cent_pylon[2], self.wall[1], self.wall_height))
        wall_list.append(AllplanGeo.Polyhedron3D.CreateCuboid(self.sec_cent_pylon[2] - self.fir_cent_pylon[2], self.wall[1], self.wall_height))
        wall_list.append(AllplanGeo.Polyhedron3D.CreateCuboid(self.thi_cent_pylon[2] - self.sec_cent_pylon[2], self.wall[1], self.wall_height))
        wall_list.append(AllplanGeo.Polyhedron3D.CreateCuboid(self.wall[0] - self.thi_cent_pylon[2], self.wall[1], self.wall_height))
        wall_list[1] = AllplanGeo.Move(wall_list[1], AllplanGeo.Vector3D(self.fir_cent_pylon[2], 0, 0))
        wall_list[2] = AllplanGeo.Move(wall_list[2], AllplanGeo.Vector3D(self.sec_cent_pylon[2], 0, 0))
        wall_list[3] = AllplanGeo.Move(wall_list[3], AllplanGeo.Vector3D(self.thi_cent_pylon[2], 0, 0))
        wall_list[0] = self.create_left_end(wall_list[0])
        wall_list[3] = self.create_right_end(wall_list[3])
        self.create_opening(self.fir_open, self.sec_open, self.thi_open, int(self.num/1000))
        self.create_opening(self.fou_open, self.fif_open, self.six_open, int(self.num/1000))
        self.create_opening(self.sev_open, self.eig_open, self.nin_open, int(self.num/1000))
        self.create_opening(self.ten_open, self.ele_open, self.twe_open, int(self.num/1000))
        if self.insul[0] or self.create_filling:
            self.create_insulation(self.fir_open, self.sec_open, self.thi_open, self.fir_sect_wall, self.sec_sect_wall, self.fir_cent_pylon[2], self.start_point, 0, 0, self.insul_type, self.num)
            self.create_insulation(self.fou_open, self.fif_open, self.six_open, self.thi_sect_wall, self.fou_sect_wall, self.sec_cent_pylon[2] - self.fir_cent_pylon[2], self.fir_cent_pylon[0], 0, self.fir_cent_pylon[2], self.insul_type, self.num+25000)
            self.create_insulation(self.sev_open, self.eig_open, self.nin_open, self.fif_sect_wall, self.six_sect_wall, self.thi_cent_pylon[2] - self.sec_cent_pylon[2], self.sec_cent_pylon[0], 0, self.sec_cent_pylon[2], self.insul_type, self.num+50000)
            self.create_insulation(self.ten_open, self.ele_open, self.twe_open, self.sev_sect_wall, self.eig_sect_wall, self.wall[0] - self.thi_cent_pylon[2], self.thi_cent_pylon[0], self.end_point, self.thi_cent_pylon[2], self.insul_type, self.num+75000)
        if not self.wall_offset[0]:
            self.create_handle(self.wall[0], self.wall[2], self.orient_params)
        else:
            wall_list[0] = AllplanGeo.Move(wall_list[0], AllplanGeo.Vector3D(self.wall[3], 0, 0))
            wall_list[1] = AllplanGeo.Move(wall_list[1], AllplanGeo.Vector3D(self.wall[3], 0, 0))
            wall_list[2] = AllplanGeo.Move(wall_list[2], AllplanGeo.Vector3D(self.wall[3], 0, 0))
            wall_list[3] = AllplanGeo.Move(wall_list[3], AllplanGeo.Vector3D(self.wall[3], 0, 0))
            self.create_handle(self.wall_offset[0], self.wall_offset[1], self.orient_params1)
            self.create_handle(self.wall[3], self.wall[4], self.orient_params)
            self.create_handle(self.wall[0] + self.wall[3], self.wall[2], self.orient_params, self.wall[3])
        wall = self.create_central_pylon(wall_list[0:2], self.fir_cent_pylon)
        wall = self.create_central_pylon([wall, wall_list[2]], self.sec_cent_pylon)
        wall = self.create_central_pylon([wall, wall_list[3]], self.thi_cent_pylon) 
        self.model_ele_list.append(AllplanBasisElements.ModelElement3D(self.com_prop, wall))

    def create_left_end(self, wall):
        if self.left_end[0] != "Пилон на торце":
            edge = Create_Edge(self.left_end[0], self.wall_height, self.left_end[1], self.wall[1], self.wall[3])
            wall, self.start_point = edge.create_edge(wall)         
            self.model_ele_list.append(edge.create_fill(self.create_filling))
        elif self.left_end[0] == "Пилон на торце":
            pylon = Create_Pylon(self.module_type, self.wall_height, self.left_end[2], self.wall[1], self.wall_orient)
            wall, self.start_point = pylon.create_pylon(wall)
            self.model_ele_list.append(pylon.create_fill(self.create_filling))           
        return wall

    def create_right_end(self, wall):
        if self.right_end[0] != "Пилон на торце":
            edge = Create_Edge(self.right_end[0], self.wall_height, self.right_end[1], self.wall[1], self.wall[3], self.wall[0])
            wall, self.end_point = edge.create_edge(wall)
            self.model_ele_list.append(edge.create_fill(self.create_filling))
        elif self.right_end[0] == "Пилон на торце":
            pylon = Create_Pylon(self.module_type, self.wall_height, self.right_end[2], self.wall[1], self.wall_orient, self.wall[0])
            wall, self.end_point = pylon.create_pylon(wall)
            self.model_ele_list.append(pylon.create_fill(self.create_filling)) 
        return wall

    def create_central_pylon(self, wall_list, pylon):             
        cent_pylon = Create_Cent_Pylon(self.module_type, self.wall_height, self.wall[1], pylon, self.wall_orient)
        wall, self.middle_point = cent_pylon.create_cent_pylon(wall_list)
        self.model_ele_list.append(cent_pylon.create_fill(self.create_filling))
        self.create_handle(pylon[2], pylon[3], self.orient_params)
        return wall

    def create_opening(self, fir_open, sec_open, thi_open, num):
        if fir_open[0]:  
            opening = Create_Opening(fir_open, self.wall[1])
            self.fixture_elements.append(opening.create_open_group_fixture(num + fir_open[7]))
            self.create_handle(fir_open[3], fir_open[5], self.orient_params)
            self.create_handle(fir_open[3] + fir_open[1], fir_open[6], self.orient_params, fir_open[3])
        if sec_open[0]:
            opening = Create_Opening(sec_open, self.wall[1])
            self.fixture_elements.append(opening.create_open_group_fixture(num + sec_open[7]))
            self.create_handle(sec_open[3], sec_open[5], self.orient_params)
            self.create_handle(sec_open[3] + sec_open[1], sec_open[6], self.orient_params, sec_open[3])
        if thi_open[0]:
            opening = Create_Opening(thi_open, self.wall[1])
            self.fixture_elements.append(opening.create_open_group_fixture(num + thi_open[7]))
            self.create_handle(thi_open[3], thi_open[5], self.orient_params)
            self.create_handle(thi_open[3] + thi_open[1], thi_open[6], self.orient_params, thi_open[3])

    def create_insulation(self, fir_open, sec_open, thi_open, fir_sect_wall, sec_sect_wall, wall_length, start_point, end_point, offset, insul_type, num):  
        insul_list = []
        fill_list = []

        fir_open = [0 if not fir_open[0] else i for i in fir_open]
        sec_open = [0 if not sec_open[0] else i for i in sec_open]
        thi_open = [0 if not thi_open[0] else i for i in thi_open]
        fir_sect_wall = [0 if not fir_sect_wall[0] else i for i in fir_sect_wall]
        sec_sect_wall = [0 if not sec_sect_wall[0] else i for i in sec_sect_wall]

        if not fir_open[0] and not sec_open[0] and not thi_open[0] and not fir_sect_wall[0] and not sec_sect_wall[0]:
            section1 = wall_length - start_point - end_point
            sect_posit1 = start_point + offset
            fill_sect1 = section1
        else:
            section1 = fir_open[3] - start_point - self.open_ver_rib_thick - offset
            sect_posit1 = start_point + offset
            fill_sect1 = fir_open[3] - start_point - offset
        fill_posit1 = sect_posit1

        if not fir_open[0]:
            section2 = fir_sect_wall[2] - start_point - offset
            sect_posit2 = start_point + offset
            fill_sect2 = fir_sect_wall[2] - start_point - offset + fir_sect_wall[1]
            fill_posit2 = sect_posit2
        else:
            section2 = fir_sect_wall[2] - fir_open[1] - fir_open[3] - self.open_ver_rib_thick
            sect_posit2 = fir_open[3] + fir_open[1] + self.open_ver_rib_thick
            fill_sect2 = fir_sect_wall[2] - fir_open[1] - fir_open[3] + fir_sect_wall[1]
            fill_posit2 = fir_open[3] + fir_open[1]

        if not fir_open[0] and not fir_sect_wall[0]:
            section3 = sec_open[3] - start_point - self.open_ver_rib_thick - offset
            sect_posit3 = start_point + offset
            fill_sect3 = sec_open[3] - start_point - offset
            fill_posit3 = sect_posit3
        elif not fir_sect_wall[0]:
            section3 = sec_open[3] - fir_open[1] - fir_open[3] - 2 * self.open_ver_rib_thick
            sect_posit3 = fir_open[3] + fir_open[1] + self.open_ver_rib_thick     
            fill_sect3 = sec_open[3] - fir_open[1] - fir_open[3]
            fill_posit3 = fir_open[3] + fir_open[1]   
        else:
            section3 = sec_open[3] - fir_sect_wall[2] - fir_sect_wall[1] - self.open_ver_rib_thick
            sect_posit3 = fir_sect_wall[2] + fir_sect_wall[1]
            fill_sect3 = sec_open[3] - fir_sect_wall[2] - fir_sect_wall[1]
            fill_posit3 = sect_posit3

        if not fir_open[0] and not fir_sect_wall[0] and not sec_open[0]:
            section4 = sec_sect_wall[2] - start_point - offset
            sect_posit4 = start_point + offset
            fill_sect4 = sec_sect_wall[2] - start_point - offset  + sec_sect_wall[1]
            fill_posit4 = sect_posit4
        elif not fir_sect_wall[0] and not sec_open[0]:
            section4 = sec_sect_wall[2] - fir_open[1] - fir_open[3] - self.open_ver_rib_thick
            sect_posit4 = fir_open[3] + fir_open[1] + self.open_ver_rib_thick 
            fill_sect4 = sec_sect_wall[2] - fir_open[1] - fir_open[3] + sec_sect_wall[1]
            fill_posit4 = fir_open[3] + fir_open[1]
        elif not sec_open[0]:
            section4 = sec_sect_wall[2] - fir_sect_wall[2] - fir_sect_wall[1]
            sect_posit4 = fir_sect_wall[2] + fir_sect_wall[1]
            fill_sect4 = sec_sect_wall[2] - fir_sect_wall[2] - fir_sect_wall[1] + sec_sect_wall[1]
            fill_posit4 = sect_posit4
        else:
            section4 = sec_sect_wall[2] - sec_open[1] - sec_open[3] - self.open_ver_rib_thick
            sect_posit4 = sec_open[3] + sec_open[1] + self.open_ver_rib_thick
            fill_sect4 = sec_sect_wall[2] - sec_open[1] - sec_open[3] + sec_sect_wall[1]
            fill_posit4 = sec_open[3] + sec_open[1]

        if not fir_open[0] and not fir_sect_wall[0] and not sec_open[0] and not sec_sect_wall[0]:
            section5 = thi_open[3] - start_point - self.open_ver_rib_thick - offset
            sect_posit5 = start_point + offset
            fill_sect5 = thi_open[3] - start_point - offset
            fill_posit5 = sect_posit5
        elif not fir_sect_wall[0] and not sec_open[0] and not sec_sect_wall[0]:
            section5 = thi_open[3] - fir_open[1] - fir_open[3] - 2 * self.open_ver_rib_thick
            sect_posit5 = fir_open[3] + fir_open[1] + self.open_ver_rib_thick
            fill_sect5 = thi_open[3] - fir_open[1] - fir_open[3]
            fill_posit5 = fir_open[3] + fir_open[1]         
        elif not sec_open[0] and not sec_sect_wall[0]:
            section5 = thi_open[3] - fir_sect_wall[2] - fir_sect_wall[1] - self.open_ver_rib_thick
            sect_posit5 = fir_sect_wall[2] + fir_sect_wall[1]
            fill_sect5 = thi_open[3] - fir_sect_wall[2] - fir_sect_wall[1]
            fill_posit5 = sect_posit5
        elif not sec_sect_wall[0]:
            section5 = thi_open[3] - sec_open[1] - sec_open[3] - 2 * self.open_ver_rib_thick
            sect_posit5 = sec_open[3] + sec_open[1] + self.open_ver_rib_thick
            fill_sect5 = thi_open[3] - sec_open[1] - sec_open[3]
            fill_posit5 = sec_open[3] + sec_open[1]
        else:
            section5 = thi_open[3]  - sec_sect_wall[2] - sec_sect_wall[1] - self.open_ver_rib_thick
            sect_posit5 = sec_sect_wall[2] + sec_sect_wall[1]
            fill_sect5 = thi_open[3]  - sec_sect_wall[2] - sec_sect_wall[1] - self.open_ver_rib_thick
            fill_posit5 = sect_posit5

        section6 = 0
        sect_posit6 = 0
        fill_sect6 = section6
        fill_posit6 = sect_posit6
        for i, elem in enumerate([fir_open, fir_sect_wall, sec_open, sec_sect_wall, thi_open]):  
            if elem[0] and not (i+1)%2:
                section6 = wall_length + offset - end_point - elem[2] - elem[1]
                sect_posit6 = elem[2] + elem[1]
                fill_sect6 = section6
                fill_posit6 = sect_posit6
            elif elem[0] and (i+1)%2:
                section6 = wall_length + offset - end_point - elem[3] - elem[1] - self.open_ver_rib_thick
                sect_posit6 = elem[3] + elem[1] + self.open_ver_rib_thick
                fill_sect6 = wall_length + offset - end_point - elem[3] - elem[1]
                fill_posit6 = elem[3] + elem[1]

        if self.insul[0]:
            fir_ver_insulation = Create_Insulation(self.rib_wall_height, section1, sect_posit1, self.slab_thick, self.hor_rib_thick, self.ver_rib_thick, self.insul)
            insul_list.extend(fir_ver_insulation.create_ver_insulation(insul_type, num))
            sec_ver_insulation = Create_Insulation(self.rib_wall_height, section2, sect_posit2, self.slab_thick, self.hor_rib_thick, self.ver_rib_thick, self.insul)
            insul_list.extend(sec_ver_insulation.create_ver_insulation(insul_type, num+2000))
            thi_ver_insulation = Create_Insulation(self.rib_wall_height, section3, sect_posit3, self.slab_thick, self.hor_rib_thick, self.ver_rib_thick, self.insul)
            insul_list.extend(thi_ver_insulation.create_ver_insulation(insul_type, num+4000))
            fou_ver_insulation = Create_Insulation(self.rib_wall_height, section4, sect_posit4, self.slab_thick, self.hor_rib_thick, self.ver_rib_thick, self.insul)
            insul_list.extend(fou_ver_insulation.create_ver_insulation(insul_type, num+6000))
            fif_ver_insulation = Create_Insulation(self.rib_wall_height, section5, sect_posit5, self.slab_thick, self.hor_rib_thick, self.ver_rib_thick, self.insul)
            insul_list.extend(fif_ver_insulation.create_ver_insulation(insul_type, num+8000))
            six_ver_insulation = Create_Insulation(self.rib_wall_height, section6, sect_posit6, self.slab_thick, self.hor_rib_thick, self.ver_rib_thick, self.insul)
            insul_list.extend(six_ver_insulation.create_ver_insulation(insul_type, num+10000))

            fir_low_hor_insulation = Create_Insulation(fir_open[4] - self.open_hor_rib_thick - self.slab_thick, fir_open[1], fir_open[3], self.slab_thick, self.hor_rib_thick, self.ver_rib_thick, self.insul)
            insul_list.extend(fir_low_hor_insulation.create_hor_insulation(insul_type, num+12000))
            sec_low_hor_insulation = Create_Insulation(sec_open[4] - self.open_hor_rib_thick - self.slab_thick, sec_open[1], sec_open[3], self.slab_thick, self.hor_rib_thick, self.ver_rib_thick, self.insul)
            insul_list.extend(sec_low_hor_insulation.create_hor_insulation(insul_type, num+14000))
            thi_low_hor_insulation = Create_Insulation(thi_open[4] - self.open_hor_rib_thick - self.slab_thick, thi_open[1], thi_open[3], self.slab_thick, self.hor_rib_thick, self.ver_rib_thick, self.insul)
            insul_list.extend(thi_low_hor_insulation.create_hor_insulation(insul_type, num+16000))
            fir_up_hor_insulation = Create_Insulation(self.rib_wall_height - fir_open[4] - fir_open[2] - self.open_hor_rib_thick + self.slab_thick, fir_open[1], fir_open[3], fir_open[4] + fir_open[2] + self.open_hor_rib_thick, self.hor_rib_thick, self.ver_rib_thick, self.insul)
            insul_list.extend(fir_up_hor_insulation.create_hor_insulation(insul_type, num+18000))
            sec_up_hor_insulation = Create_Insulation(self.rib_wall_height - sec_open[4] - sec_open[2] - self.open_hor_rib_thick + self.slab_thick, sec_open[1], sec_open[3], sec_open[4] + sec_open[2] + self.open_hor_rib_thick, self.hor_rib_thick, self.ver_rib_thick, self.insul)
            insul_list.extend(sec_up_hor_insulation.create_hor_insulation(insul_type, num+20000))
            thi_up_hor_insulation = Create_Insulation(self.rib_wall_height - thi_open[4] - thi_open[2] - self.open_hor_rib_thick + self.slab_thick, thi_open[1], thi_open[3], thi_open[4] + thi_open[2] + self.open_hor_rib_thick, self.hor_rib_thick, self.ver_rib_thick, self.insul)
            insul_list.extend(thi_up_hor_insulation.create_hor_insulation(insul_type, num+22000))

        if self.create_filling:
            fill_list.append(Create_Insulation.create_fill(fill_sect1, self.wall[1], fill_posit1, self.create_filling))
            fill_list.append(Create_Insulation.create_fill(fill_sect2, self.wall[1], fill_posit2, self.create_filling))
            fill_list.append(Create_Insulation.create_fill(fill_sect3, self.wall[1], fill_posit3, self.create_filling))
            fill_list.append(Create_Insulation.create_fill(fill_sect4, self.wall[1], fill_posit4, self.create_filling))
            fill_list.append(Create_Insulation.create_fill(fill_sect5, self.wall[1], fill_posit5, self.create_filling))
            fill_list.append(Create_Insulation.create_fill(fill_sect6, self.wall[1], fill_posit6, self.create_filling))

        self.model_ele_list.extend(fill for fill in fill_list) 
        self.fixture_elements.extend(insul for insul in insul_list)
        #self.library_ele_list.extend(fir_ver_insulation.create_ribb_reinf(self.orient_params, self.wall[1]))
        if fir_sect_wall[0]:
            self.create_handle(fir_sect_wall[2], fir_sect_wall[3], self.orient_params)
        if sec_sect_wall[0]:
            self.create_handle(sec_sect_wall[2], sec_sect_wall[3], self.orient_params)

    def create_handle(self, handle_end_point, handle_name, orient_params, handle_origin_point=0):
        origin = AllplanGeo.Point3D(handle_origin_point * m.cos(m.radians(orient_params[3])) + orient_params[1], handle_origin_point * m.sin(m.radians(orient_params[3])) + orient_params[2], 0)
        end = AllplanGeo.Point3D(handle_end_point * m.cos(m.radians(orient_params[3])) + orient_params[1], handle_end_point * m.sin(m.radians(orient_params[3])) + orient_params[2], 0)
        handle = HandleProperties(str(handle_name), end, origin, [(handle_name, orient_params[0])], orient_params[0], True)
        self.handle_list.append(handle)


class Create_Edge():
    def __init__(self, edge_type, wall_height, edge_length, wall_thick, edge_offset, wall_length = None):
        self.edge_type = edge_type
        self.wall_height = wall_height
        self.wall_thick = wall_thick
        self.edge_length = edge_length
        self.wall_length = wall_length
        self.edge_offset = edge_offset

    def create_edge(self, wall):
        if self.edge_type == "Торец базовый":
            return wall, self.edge_length
        elif self.edge_type == "Торец без подрезки":
            return self.create_edge_without_undercut(wall)
        elif self.edge_type == "Торец с подрезкой":
            return self.create_edge_with_undercut(wall)

    def create_edge_without_undercut(self, wall):
        if not self.edge_offset:
            subtract_volume = AllplanGeo.Polyhedron3D.CreateCuboid(self.wall_thick, self.wall_thick, self.wall_height)
            if self.wall_length:
                subtract_volume = AllplanGeo.Move(subtract_volume, AllplanGeo.Vector3D(self.wall_length - self.wall_thick, 0, 0))
            _, wall = AllplanGeo.MakeSubtraction(wall, subtract_volume)
            point = self.edge_length + self.wall_thick
            return wall, point
        else:
            point = self.edge_length + self.edge_offset
            if self.wall_length:
                point = self.edge_length - self.edge_offset
            return wall, point

    def create_edge_with_undercut(self, wall):
        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(0, 0, 0)
        base_pol += AllplanGeo.Point3D(20, 0, 0)
        base_pol += AllplanGeo.Point3D(20, 0, 60)
        base_pol += AllplanGeo.Point3D(0, 0, 60)
        base_pol += AllplanGeo.Point3D(0, 0, 0)

        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(0, 0, 0)
        path += AllplanGeo.Point3D(0, self.wall_thick, 0)

        _, subtract_volume1 = AllplanGeo.CreatePolyhedron(base_pol, path)
        
        if not self.edge_offset:
            subtract_volume1 = AllplanGeo.Move(subtract_volume1, AllplanGeo.Vector3D(self.wall_thick, 0, 0))
            subtract_volume2 = AllplanGeo.Polyhedron3D.CreateCuboid(self.wall_thick, self.wall_thick, self.wall_height)
            if self.wall_length:
                subtract_volume1 = AllplanGeo.Mirror(subtract_volume1, AllplanGeo.Axis2D(AllplanGeo.Point2D(), AllplanGeo.Vector2D(0, 1)))
                subtract_volume1 = AllplanGeo.Move(subtract_volume1, AllplanGeo.Vector3D(self.wall_length, 0, 0))
                subtract_volume2 = AllplanGeo.Move(subtract_volume2, AllplanGeo.Vector3D(self.wall_length - self.wall_thick, 0, 0))      
            _, wall = AllplanGeo.MakeSubtraction(wall, subtract_volume1)
            _, wall = AllplanGeo.MakeSubtraction(wall, subtract_volume2)
            point = self.edge_length + self.wall_thick
            return wall, point
        else:
            point = self.edge_length + self.edge_offset
            if self.wall_length:
                subtract_volume1 = AllplanGeo.Mirror(subtract_volume1, AllplanGeo.Axis2D(AllplanGeo.Point2D(), AllplanGeo.Vector2D(0, 1)))
                subtract_volume1 = AllplanGeo.Move(subtract_volume1, AllplanGeo.Vector3D(self.wall_length, 0, 0))   
                point = self.edge_length - self.edge_offset
            _, wall = AllplanGeo.MakeSubtraction(wall, subtract_volume1)
            return wall, point
       
    def create_fill(self, create_filling):  
        if not create_filling:
            return None

        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()
        com_prop.Layer = 3717
        color = AllplanBasisElements.ARGB (180, 180, 180, 0)
        props = AllplanBasisElements.FillingProperties()
        props.FirstColor = color

        polygon = AllplanGeo.Polygon2D()
        polygon += AllplanGeo.Point2D(0, 0)
        polygon += AllplanGeo.Point2D(self.edge_length, 0)
        polygon += AllplanGeo.Point2D(self.edge_length, self.wall_thick)
        polygon += AllplanGeo.Point2D(self.edge_length, self.wall_thick)
        polygon += AllplanGeo.Point2D(0, self.wall_thick)
        polygon += AllplanGeo.Point2D(0, 0)
        
        x_offset = self.wall_thick
        if self.edge_type == "Торец базовый":
            x_offset = 0

        if not self.edge_offset:
            polygon = AllplanGeo.Move(polygon, AllplanGeo.Vector2D(x_offset, 0))
            if self.wall_length:
                polygon = AllplanGeo.Move(polygon, AllplanGeo.Vector2D(self.wall_length - self.edge_length - 2 * x_offset, 0))
        else:
            polygon = AllplanGeo.Move(polygon, AllplanGeo.Vector2D(self.edge_offset, 0))
            if self.wall_length:
                polygon = AllplanGeo.Move(polygon, AllplanGeo.Vector2D(self.wall_length - self.edge_length, 0))
        return AllplanBasisElements.FillingElement(com_prop, props, polygon)


class Create_Pylon():
    def __init__(self, module_type, wall_height, pylon_length, wall_thick, wall_orient, wall_length = None):
        self.module_type = module_type
        self.wall_height = wall_height
        self.wall_thick = wall_thick
        self.pylon_length = pylon_length
        self.wall_length = wall_length
        self.wall_orient = wall_orient
        self.library_ele_list = []

    def create_pylon(self, wall):
        if self.module_type == "Для типового этажа":
            return self.create_typical_pylon(wall)
        elif self.module_type == "Для подземного/первого этажа":
            return self.create_ground_pylon(wall)
        elif self.module_type == "Для малоэтажных зданий":
            return self.create_low_rise_pylon(wall)

    def create_typical_pylon(self, wall):
        base_pol1 = AllplanGeo.Polygon3D()
        base_pol1 += AllplanGeo.Point3D(0, 0, 0)
        base_pol1 += AllplanGeo.Point3D(self.pylon_length + 62, 0, 0)
        base_pol1 += AllplanGeo.Point3D(self.pylon_length + 12, 0, 50)
        base_pol1 += AllplanGeo.Point3D(0, 0, 50)
        base_pol1 += AllplanGeo.Point3D(0, 0, 0)

        base_pol2 = AllplanGeo.Polygon3D()
        base_pol2 += AllplanGeo.Point3D(0, 0, self.wall_height)
        base_pol2 += AllplanGeo.Point3D(self.pylon_length + 60, 0, self.wall_height)
        base_pol2 += AllplanGeo.Point3D(self.pylon_length, 0, self.wall_height + 60)
        base_pol2 += AllplanGeo.Point3D(0, 0, self.wall_height + 60)
        base_pol2 += AllplanGeo.Point3D(0, 0, self.wall_height)

        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(0, 0, 0)
        path += AllplanGeo.Point3D(0, self.wall_thick, 0)

        _, subtract_volume = AllplanGeo.CreatePolyhedron(base_pol1, path)
        _, union_volume = AllplanGeo.CreatePolyhedron(base_pol2, path)
        if self.wall_length:
            subtract_volume = AllplanGeo.Mirror(subtract_volume, AllplanGeo.Axis2D(AllplanGeo.Point2D(), AllplanGeo.Vector2D(0, 1)))
            subtract_volume = AllplanGeo.Move(subtract_volume, AllplanGeo.Vector3D(self.wall_length, 0, 0))
            union_volume = AllplanGeo.Mirror(union_volume, AllplanGeo.Axis2D(AllplanGeo.Point2D(), AllplanGeo.Vector2D(0, 1)))
            union_volume = AllplanGeo.Move(union_volume, AllplanGeo.Vector3D(self.wall_length, 0, 0))

        _, wall = AllplanGeo.MakeSubtraction(wall, subtract_volume)
        _, wall = AllplanGeo.MakeUnion(wall, union_volume)
        return wall, self.pylon_length 

    def create_ground_pylon(self, wall):
        base_pol1 = AllplanGeo.Polygon3D()
        base_pol1 += AllplanGeo.Point3D(0, 0, self.wall_height)
        base_pol1 += AllplanGeo.Point3D(self.pylon_length + 60, 0, self.wall_height)
        base_pol1 += AllplanGeo.Point3D(self.pylon_length, 0, self.wall_height + 60)
        base_pol1 += AllplanGeo.Point3D(0, 0, self.wall_height + 60)
        base_pol1 += AllplanGeo.Point3D(0, 0, self.wall_height)

        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(0, 0, 0)
        path += AllplanGeo.Point3D(0, self.wall_thick, 0)

        _, union_volume = AllplanGeo.CreatePolyhedron(base_pol1, path)
        if self.wall_length:
            union_volume = AllplanGeo.Mirror(union_volume, AllplanGeo.Axis2D(AllplanGeo.Point2D(), AllplanGeo.Vector2D(0, 1)))
            union_volume = AllplanGeo.Move(union_volume, AllplanGeo.Vector3D(self.wall_length, 0, 0))

        _, wall = AllplanGeo.MakeUnion(wall, union_volume)
        return wall, self.pylon_length 

    def create_low_rise_pylon(self, wall):
        base_pol1 = AllplanGeo.Polygon3D()
        base_pol1 += AllplanGeo.Point3D(0, 0, self.wall_height)
        base_pol1 += AllplanGeo.Point3D(self.pylon_length, 0, self.wall_height)
        base_pol1 += AllplanGeo.Point3D(self.pylon_length, 0, self.wall_height + 20)
        base_pol1 += AllplanGeo.Point3D(0, 0, self.wall_height + 20)
        base_pol1 += AllplanGeo.Point3D(0, 0, self.wall_height)

        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(0, 0, 0)
        path += AllplanGeo.Point3D(0, self.wall_thick, 0)

        _, union_volume = AllplanGeo.CreatePolyhedron(base_pol1, path)
        if self.wall_length:
            union_volume = AllplanGeo.Mirror(union_volume, AllplanGeo.Axis2D(AllplanGeo.Point2D(), AllplanGeo.Vector2D(0, 1)))
            union_volume = AllplanGeo.Move(union_volume, AllplanGeo.Vector3D(self.wall_length, 0, 0))

        _, wall = AllplanGeo.MakeUnion(wall, union_volume)
        return wall, self.pylon_length 

    def create_fill(self, create_filling):
        if not create_filling:
            return None

        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()
        com_prop.Layer = 3717
        color = AllplanBasisElements.ARGB (0, 0, 0, 0)
        props = AllplanBasisElements.FillingProperties()
        props.FirstColor = color

        polygon = AllplanGeo.Polygon2D()
        polygon += AllplanGeo.Point2D(0, 0)
        polygon += AllplanGeo.Point2D(self.pylon_length, 0)
        polygon += AllplanGeo.Point2D(self.pylon_length, self.wall_thick)
        polygon += AllplanGeo.Point2D(self.pylon_length, self.wall_thick)
        polygon += AllplanGeo.Point2D(0, self.wall_thick)
        polygon += AllplanGeo.Point2D(0, 0)

        if self.wall_length:
            polygon = AllplanGeo.Move(polygon, AllplanGeo.Vector2D(self.wall_length - self.pylon_length, 0))
        return AllplanBasisElements.FillingElement(com_prop, props, polygon)


class Create_Cent_Pylon():   
    def __init__(self, module_type, wall_height, wall_thick, cent_pylon, wall_orient):
        self.module_type = module_type
        self.wall_height = wall_height
        self.wall_thick = wall_thick
        self.cent_pylon_length = cent_pylon[0]
        self.cent_pylon_thick = cent_pylon[1]
        self.cent_pylon_posit = cent_pylon[2]
        self.wall_orient = wall_orient
        self.library_ele_list = []

    def create_cent_pylon(self, wall_list):
        if self.module_type == "Для типового этажа":
            return self.create_typical_cent_pylon(wall_list)
        elif self.module_type == "Для подземного/первого этажа":
            return self.create_ground_cent_pylon(wall_list)
        elif self.module_type == "Для малоэтажных зданий":
            return self.create_low_rise_cent_pylon(wall_list)

    def create_typical_cent_pylon(self, wall_list):
        base_pol1 = AllplanGeo.Polygon3D()
        base_pol1 += AllplanGeo.Point3D(-62, 0, 0)
        base_pol1 += AllplanGeo.Point3D(-12, 0, 50)
        base_pol1 += AllplanGeo.Point3D(self.cent_pylon_length + 12, 0, 50)
        base_pol1 += AllplanGeo.Point3D(self.cent_pylon_length + 62, 0, 0)
        base_pol1 += AllplanGeo.Point3D(-62, 0, 0)

        base_pol2 = AllplanGeo.Polygon3D()
        base_pol2 += AllplanGeo.Point3D(-60, 0, self.wall_height)
        base_pol2 += AllplanGeo.Point3D(0, 0, self.wall_height + 60)
        base_pol2 += AllplanGeo.Point3D(self.cent_pylon_length, 0, self.wall_height + 60)
        base_pol2 += AllplanGeo.Point3D(self.cent_pylon_length + 60, 0, self.wall_height)
        base_pol2 += AllplanGeo.Point3D(-60, 0, self.wall_height)

        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(0, 0, 0)
        path += AllplanGeo.Point3D(0, self.wall_thick, 0)

        _, subtract_volume = AllplanGeo.CreatePolyhedron(base_pol1, path)
        _, union_volume1 = AllplanGeo.CreatePolyhedron(base_pol2, path)
        union_volume2 = AllplanGeo.Polyhedron3D.CreateCuboid(self.cent_pylon_length, self.cent_pylon_thick, self.wall_height + 10)

        subtract_volume = AllplanGeo.Move(subtract_volume, AllplanGeo.Vector3D(self.cent_pylon_posit, 0, 0))
        union_volume1 = AllplanGeo.Move(union_volume1, AllplanGeo.Vector3D(self.cent_pylon_posit, 0, 0))
        union_volume2 = AllplanGeo.Move(union_volume2, AllplanGeo.Vector3D(self.cent_pylon_posit, 0, 50))

        _, wall = AllplanGeo.MakeUnion(wall_list[0], wall_list[1])
        _, wall = AllplanGeo.MakeSubtraction(wall, subtract_volume)
        _, wall = AllplanGeo.MakeUnion(wall, union_volume1)  
        _, wall = AllplanGeo.MakeUnion(wall, union_volume2)
        return wall, self.cent_pylon_length + self.cent_pylon_posit

    def create_ground_cent_pylon(self, wall_list):
        base_pol1 = AllplanGeo.Polygon3D()
        base_pol1 += AllplanGeo.Point3D(-60, 0, self.wall_height)
        base_pol1 += AllplanGeo.Point3D(0, 0, self.wall_height + 60)
        base_pol1 += AllplanGeo.Point3D(self.cent_pylon_length, 0, self.wall_height + 60)
        base_pol1 += AllplanGeo.Point3D(self.cent_pylon_length + 60, 0, self.wall_height)
        base_pol1 += AllplanGeo.Point3D(-60, 0, self.wall_height)

        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(0, 0, 0)
        path += AllplanGeo.Point3D(0, self.wall_thick, 0)
 
        _, union_volume1 = AllplanGeo.CreatePolyhedron(base_pol1, path)
        union_volume2 = AllplanGeo.Polyhedron3D.CreateCuboid(self.cent_pylon_length, self.cent_pylon_thick, self.wall_height + 60)

        union_volume1 = AllplanGeo.Move(union_volume1, AllplanGeo.Vector3D(self.cent_pylon_posit, 0, 0))
        union_volume2 = AllplanGeo.Move(union_volume2, AllplanGeo.Vector3D(self.cent_pylon_posit, 0, 0))
      
        _, wall = AllplanGeo.MakeUnion(wall_list[0], wall_list[1])
        _, wall = AllplanGeo.MakeUnion(wall, union_volume1)
        _, wall = AllplanGeo.MakeUnion(wall, union_volume2)
        return wall, self.cent_pylon_length + self.cent_pylon_posit

    def create_low_rise_cent_pylon(self, wall_list):
        base_pol1 = AllplanGeo.Polygon3D()
        base_pol1 += AllplanGeo.Point3D(0, 0, self.wall_height)
        base_pol1 += AllplanGeo.Point3D(0, 0, self.wall_height + 20)
        base_pol1 += AllplanGeo.Point3D(self.cent_pylon_length, 0, self.wall_height + 20)
        base_pol1 += AllplanGeo.Point3D(self.cent_pylon_length, 0, self.wall_height)
        base_pol1 += AllplanGeo.Point3D(0, 0, self.wall_height)

        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(0, 0, 0)
        path += AllplanGeo.Point3D(0, self.wall_thick, 0)
 
        _, union_volume1 = AllplanGeo.CreatePolyhedron(base_pol1, path)
        union_volume2 = AllplanGeo.Polyhedron3D.CreateCuboid(self.cent_pylon_length, self.cent_pylon_thick, self.wall_height + 20)

        union_volume1 = AllplanGeo.Move(union_volume1, AllplanGeo.Vector3D(self.cent_pylon_posit, 0, 0))
        union_volume2 = AllplanGeo.Move(union_volume2, AllplanGeo.Vector3D(self.cent_pylon_posit, 0, 0))
      
        _, wall = AllplanGeo.MakeUnion(wall_list[0], wall_list[1])
        _, wall = AllplanGeo.MakeUnion(wall, union_volume1)  
        _, wall = AllplanGeo.MakeUnion(wall, union_volume2)
        return wall, self.cent_pylon_length + self.cent_pylon_posit

    def create_fill(self, create_filling):
        if not create_filling:
            return None

        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()
        com_prop.Layer = 3717
        color = AllplanBasisElements.ARGB (0, 0, 0, 0)
        props = AllplanBasisElements.FillingProperties()
        props.FirstColor = color

        polygon = AllplanGeo.Polygon2D()
        polygon += AllplanGeo.Point2D(0, 0)
        polygon += AllplanGeo.Point2D(self.cent_pylon_length, 0)
        polygon += AllplanGeo.Point2D(self.cent_pylon_length, self.cent_pylon_thick)
        polygon += AllplanGeo.Point2D(self.cent_pylon_length, self.cent_pylon_thick)
        polygon += AllplanGeo.Point2D(0, self.cent_pylon_thick)
        polygon += AllplanGeo.Point2D(0, 0)
        
        polygon = AllplanGeo.Move(polygon, AllplanGeo.Vector2D(self.cent_pylon_posit, 0))
        return AllplanBasisElements.FillingElement(com_prop, props, polygon)


class Create_Opening():

    def __init__(self, opening, wall_thick):
        self.open_width = opening[1]
        self.open_height = opening[2]
        self.open_x_posit = opening[3]
        self.open_z_posit = opening[4]   
        self.wall_thick = wall_thick
        
        self.com_prop = AllplanBaseElements.CommonProperties()
        self.com_prop.GetGlobalProperties()
        self.com_prop.ColorByLayer = False
        self.com_prop.Layer = 62622
        self.com_prop.Pen = 15 
        self.com_prop.Color = 1

    def create_open_group_fixture(self, num): 
        attr_list = []
        attr_set_list = []
        
        location = AllplanGeo.Point3D(self.open_x_posit, 0, self.open_z_posit + 300)
        symbol_prop = AllplanBasisElements.Symbol3DProperties()
        symbol_prop.SymbolID = 1
        symbol_prop.Height = 1
        symbol_prop.Width = 1
        symbol_list = [AllplanBasisElements.Symbol3DElement(self.com_prop, symbol_prop, location)]

        sym_slide_prop = AllplanPrecast.FixtureSlideProperties()
        sym_slide_prop.ViewType = AllplanPrecast.FixtureSlideViewType.eCONNECTION_POINT
        slide_list = [AllplanPrecast.FixtureSlideElement(sym_slide_prop, symbol_list)]      
              
        fix_macro_grp_prop = AllplanPrecast.FixtureProperties()
        fix_macro_grp_prop.Type = AllplanPrecast.MacroType.eGroup_Fixture 
        fix_macro_grp = AllplanPrecast.FixtureElement(fix_macro_grp_prop, slide_list)
        fix_macro_grp.SetHash(hashlib.sha224(str(fix_macro_grp).encode('utf-8')).hexdigest())
         
        fixture_grp_pl_prop = AllplanPrecast.FixturePlacementProperties()
        fixture_grp_pl_prop.Name = "Проем (т.160)" + str(num)
        fixtureGrp = AllplanPrecast.FixturePlacementElement(self.com_prop, fixture_grp_pl_prop, fix_macro_grp)
   
        attr_list.append(AllplanBaseElements.AttributeInteger(1013, 0))
        attr_set_list.append(AllplanBaseElements.AttributeSet(attr_list))
        attributes = AllplanBaseElements.Attributes(attr_set_list)
       
        group_list = [fixtureGrp]
        group_list.append(self.create_fir_open_fixture(num))
        group_list.append(self.create_sec_open_fixture(num))
        group_list.append(self.create_thi_open_fixture(num))

        fixture_grp_prop = AllplanPrecast.FixtureGroupProperties()
        fixture_grp_prop.Name = "Проем (т.160)"
        group = AllplanPrecast.FixtureGroupElement(fixture_grp_prop, group_list)
        group.SetAttributes(attributes)
        return group
            
    def create_fir_open_fixture(self, num):    
        symbol_list = [] 
        open_slides = []
        attr_list = []
        attr_set_list = []
        
        opening = AllplanGeo.Polyhedron3D.CreateCuboid(self.open_width, self.wall_thick, self.open_height)
        open_slide_3d = [AllplanBasisElements.ModelElement3D(self.com_prop, opening)]

        location1 = AllplanGeo.Point3D(0, 0, 0)
        location2 = AllplanGeo.Point3D(self.open_width, 0, 0)
        location3 = AllplanGeo.Point3D(self.open_width, 0, self.open_height)
        location4 = AllplanGeo.Point3D(0, 0, self.open_height)
        location5 = AllplanGeo.Point3D(0, self.wall_thick, 0)
        location6 = AllplanGeo.Point3D(self.open_width, self.wall_thick, 0)
        location7 = AllplanGeo.Point3D(self.open_width, self.wall_thick, self.open_height)
        location8 = AllplanGeo.Point3D(0, self.wall_thick, self.open_height)
        
        symbol_prop = AllplanBasisElements.Symbol3DProperties()
        symbol_prop.SymbolID = 1;
        symbol_prop.Height = 1
        symbol_prop.Width = 1

        symbol1 = AllplanBasisElements.Symbol3DElement(self.com_prop, symbol_prop, location1)
        symbol2 = AllplanBasisElements.Symbol3DElement(self.com_prop, symbol_prop, location2)
        symbol3 = AllplanBasisElements.Symbol3DElement(self.com_prop, symbol_prop, location3)
        symbol4 = AllplanBasisElements.Symbol3DElement(self.com_prop, symbol_prop, location4)
        symbol5 = AllplanBasisElements.Symbol3DElement(self.com_prop, symbol_prop, location5)
        symbol6 = AllplanBasisElements.Symbol3DElement(self.com_prop, symbol_prop, location6)
        symbol7 = AllplanBasisElements.Symbol3DElement(self.com_prop, symbol_prop, location7)
        symbol8 = AllplanBasisElements.Symbol3DElement(self.com_prop, symbol_prop, location8)               
        
        symbol_list.extend([symbol1, symbol2, symbol3, symbol4, symbol5, symbol6, symbol7, symbol8]) 

        open_slide_prop_3d = AllplanPrecast.FixtureSlideProperties()
        open_slide_prop_3d.ViewType = AllplanPrecast.FixtureSlideViewType.e3D_VIEW
        open_slides.append(AllplanPrecast.FixtureSlideElement(open_slide_prop_3d, open_slide_3d))    

        sym_slide_prop = AllplanPrecast.FixtureSlideProperties()
        sym_slide_prop.ViewType = AllplanPrecast.FixtureSlideViewType.eMEASURE_POINTS
        open_slides.append(AllplanPrecast.FixtureSlideElement(sym_slide_prop, symbol_list))
            
        open_fixture_prop = AllplanPrecast.FixtureProperties()
        open_fixture_prop.Type = AllplanPrecast.MacroType.ePoint_Fixture
        open_fixture_prop.Name = "Проем(размеры)" + str(num)     
        open_fixture = AllplanPrecast.FixtureElement(open_fixture_prop, open_slides)
        open_fixture.SetHash(hashlib.sha224(str(open_fixture).encode('utf-8')).hexdigest())

        open_fixture_place_prop = AllplanPrecast.FixturePlacementProperties()
        open_fixture_place_prop.Name = "Проем(размеры)"
        open_fixture_place_prop.ConnectionToAIACatalog = True
        
        attr_list.append(AllplanBaseElements.AttributeString(1332, "Платик_Проем"))
        attr_list.append(AllplanBaseElements.AttributeInteger(1013, 11))
        attr_set_list.append(AllplanBaseElements.AttributeSet(attr_list))
        attributes = AllplanBaseElements.Attributes(attr_set_list)
        
        open_fixture_place = AllplanPrecast.FixturePlacementElement(self.com_prop, open_fixture_place_prop, open_fixture)
        open_fixture_place.SetAttributes(attributes)
        AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(self.open_x_posit, 0, self.open_z_posit), 0.,0.,0., [open_fixture_place])
        return open_fixture_place

    def create_sec_open_fixture(self, num):    
        line_list1 = []
        line_list2 = []
        line_list3 = []
        open_slides = []
        attr_list = []
        attr_set_list = []
        
        opening = AllplanGeo.Polyhedron3D.CreateCuboid(self.open_width, self.wall_thick, self.open_height)
        open_slide_3d = [AllplanBasisElements.ModelElement3D(self.com_prop, opening)]
        
        point1 = AllplanGeo.Point2D(0, 0)
        point2 = AllplanGeo.Point2D(self.open_width, self.wall_thick)
        point3 = AllplanGeo.Point2D(0, self.wall_thick)
        point4 = AllplanGeo.Point2D(self.open_width, 0)
        point5 = AllplanGeo.Point2D(0, 0)
        point6 = AllplanGeo.Point2D(100, self.open_height - 100)
        point7 = AllplanGeo.Point2D(self.open_width, self.open_height)
        
        line1 = AllplanGeo.Line2D(point1, point2)
        line2 = AllplanGeo.Line2D(point3, point4)
        line3 = AllplanGeo.Line2D(point5, point6)
        line4 = AllplanGeo.Line2D(point6, point7)

        polygon1 = AllplanGeo.Polygon2D()
        polygon1 += AllplanGeo.Point2D(0, 0)
        polygon1 += AllplanGeo.Point2D(self.open_width, 0)
        polygon1 += AllplanGeo.Point2D(self.open_width, self.open_height)
        polygon1 += AllplanGeo.Point2D(0, self.open_height)
        polygon1 += AllplanGeo.Point2D(0, 0)

        line5 = AllplanGeo.Move(line3, AllplanGeo.Vector2D(-self.open_width, 0))
        line6 = AllplanGeo.Move(line4, AllplanGeo.Vector2D(-self.open_width, 0))
        polygon2 = AllplanGeo.Move(polygon1, AllplanGeo.Vector2D(-self.open_width, 0))

        line_list1.append(AllplanBasisElements.ModelElement2D(self.com_prop, line1))
        line_list1.append(AllplanBasisElements.ModelElement2D(self.com_prop, line2))
        line_list2.append(AllplanBasisElements.ModelElement2D(self.com_prop, line3))
        line_list2.append(AllplanBasisElements.ModelElement2D(self.com_prop, line4))
        line_list2.append(AllplanBasisElements.ModelElement2D(self.com_prop, polygon1))
        line_list3.append(AllplanBasisElements.ModelElement2D(self.com_prop, line5))
        line_list3.append(AllplanBasisElements.ModelElement2D(self.com_prop, line6))
        line_list3.append(AllplanBasisElements.ModelElement2D(self.com_prop, polygon2))
        
        open_slide_prop_3d = AllplanPrecast.FixtureSlideProperties()
        open_slide_prop_3d.VisibilityGeo2D = False
        open_slide_prop_3d.ViewType = AllplanPrecast.FixtureSlideViewType.e3D_VIEW
        open_slides.append(AllplanPrecast.FixtureSlideElement(open_slide_prop_3d, open_slide_3d))

        open_slide_prop_2d_top = AllplanPrecast.FixtureSlideProperties()
        open_slide_prop_2d_top.VisibilityGeo3D = False
        open_slide_prop_2d_top.ViewType = AllplanPrecast.FixtureSlideViewType.e2D_TOP_VIEW
        open_slides.append(AllplanPrecast.FixtureSlideElement(open_slide_prop_2d_top, line_list1))

        open_slide_prop_2d_front = AllplanPrecast.FixtureSlideProperties()
        open_slide_prop_2d_front.VisibilityGeo3D = False
        open_slide_prop_2d_front.ViewType = AllplanPrecast.FixtureSlideViewType.e2D_FRONT_VIEW
        open_slides.append(AllplanPrecast.FixtureSlideElement(open_slide_prop_2d_front, line_list2))   

        open_slide_prop_2d_back = AllplanPrecast.FixtureSlideProperties()
        open_slide_prop_2d_back.VisibilityGeo3D = False
        open_slide_prop_2d_back.ViewType = AllplanPrecast.FixtureSlideViewType.e2D_BACK_VIEW
        open_slides.append(AllplanPrecast.FixtureSlideElement(open_slide_prop_2d_back, line_list3)) 
            
        open_fixture_prop = AllplanPrecast.FixtureProperties()
        open_fixture_prop.Type = AllplanPrecast.MacroType.ePoint_Fixture
        open_fixture_prop.Name = "Проем(крест)" + str(num)    
        open_fixture = AllplanPrecast.FixtureElement(open_fixture_prop, open_slides)
        open_fixture.SetHash(hashlib.sha224(str(open_fixture).encode('utf-8')).hexdigest())

        open_fixture_place_prop = AllplanPrecast.FixturePlacementProperties()
        open_fixture_place_prop.Name = "Проем(крест)"
        open_fixture_place_prop.ConnectionToAIACatalog = True
        
        attr_list.append(AllplanBaseElements.AttributeString(1332, "Крест_Проем"))
        attr_list.append(AllplanBaseElements.AttributeInteger(1013, 12))
        attr_set_list.append(AllplanBaseElements.AttributeSet(attr_list))
        attributes = AllplanBaseElements.Attributes(attr_set_list)
        
        open_fixture_place = AllplanPrecast.FixturePlacementElement(self.com_prop, open_fixture_place_prop, open_fixture)
        open_fixture_place.SetAttributes(attributes)
        AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(self.open_x_posit, 0, self.open_z_posit), 0.,0.,0., [open_fixture_place])
        return open_fixture_place
    
    def create_thi_open_fixture(self, num):    
        open_slides = []
        attr_list = []
        attr_set_list = []
 
        opening = AllplanGeo.Polyhedron3D.CreateCuboid(self.open_width, self.wall_thick, self.open_height)
        open_slide_3d = [AllplanBasisElements.ModelElement3D(self.com_prop, opening)]

        point1 = AllplanGeo.Point3D(0, 0, 0)
        point2 = AllplanGeo.Point3D(0, 0, self.open_height)
        line = AllplanGeo.Line3D(point1, point2)
        line_list = [AllplanBasisElements.ModelElement3D(self.com_prop, line)]

        open_slide_prop_3d = AllplanPrecast.FixtureSlideProperties()
        open_slide_prop_3d.ViewType = AllplanPrecast.FixtureSlideViewType.e3D_VIEW
        open_slides.append(AllplanPrecast.FixtureSlideElement(open_slide_prop_3d, line_list)) 
        
        open_slide_prop_out_vol = AllplanPrecast.FixtureSlideProperties()
        open_slide_prop_out_vol.ViewType = AllplanPrecast.FixtureSlideViewType.e3D_VIEW_OUTLINE_VOLUME
        open_slides.append(AllplanPrecast.FixtureSlideElement(open_slide_prop_out_vol, open_slide_3d))    

        open_fixture_prop = AllplanPrecast.FixtureProperties()
        open_fixture_prop.Type = AllplanPrecast.MacroType.eLine_Fixture
        open_fixture_prop.SubType = AllplanPrecast.MacroSubType.ePrefabModeller
        open_fixture_prop.Name = "BftModellierer" + str(num)   
        open_fixture = AllplanPrecast.FixtureElement(open_fixture_prop, open_slides)
        open_fixture.SetHash(hashlib.sha224(str(open_fixture).encode('utf-8')).hexdigest())

        open_fixture_place_prop = AllplanPrecast.FixturePlacementProperties()
        open_fixture_place_prop.Name = "BftModellierer"
        open_fixture_place_prop.OutlineType = AllplanPrecast.OutlineType.eBUILTIN_OUTLINE_TYPE_MINUS
        open_fixture_place_prop.OutlineTypeInGroup = AllplanPrecast.OutlineTypeInGroup.eBUILTIN_OUTLINE_TYPE_IN_GROUP_MINUS
        open_fixture_place_prop.OutlineShape = AllplanPrecast.OutlineShape.eBUILTIN_OUTLINE_SHAPE_SYMBOL

        attr_set_list.append(AllplanBaseElements.AttributeSet(attr_list))
        attributes = AllplanBaseElements.Attributes(attr_set_list)
        
        open_fixture_place = AllplanPrecast.FixturePlacementElement(self.com_prop, open_fixture_place_prop, open_fixture)
        open_fixture_place.SetAttributes(attributes)
        AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(self.open_x_posit, 0, self.open_z_posit), 0.,0.,0., [open_fixture_place])
        return open_fixture_place

    
class Create_Insulation():

    def __init__(self, wall_height, wall_length, start_point, z_start_point, hor_rib_thick, ver_rib_thick, insul):
        self.wall_height = wall_height
        self.wall_length = wall_length
        self.insul = [insul[1], insul[2], insul[3], insul[4]]
        self.hor_rib_thick = hor_rib_thick
        self.ver_rib_thick = ver_rib_thick
        self.start_point = start_point
        self.z_start_point = z_start_point
 
        self.com_prop = AllplanBaseElements.CommonProperties()
        self.com_prop.GetGlobalProperties()
        self.com_prop.ColorByLayer = False
        self.com_prop.Layer = 3922
        self.com_prop.Pen = 7 
        self.com_prop.Color = 4

        self.com_prop1 = AllplanBaseElements.CommonProperties()
        self.com_prop1.GetGlobalProperties()
        self.com_prop1.ColorByLayer = False
        self.com_prop1.Layer = 3922
        self.com_prop1.Pen = 11 
        self.com_prop1.Color = 1
 
    def create_ver_insulation(self, insul_type, num, position = False):
        insul_fix_list = []
        if self.wall_length <= 0:
            return insul_fix_list
        
        num_z_step = self.wall_height // (self.insul[1] + self.hor_rib_thick)
        z_resid = self.wall_height % (self.insul[1] + self.hor_rib_thick)
        if z_resid > self.insul[1]:
            z_resid = self.insul[1]
        
        num_x_step = self.wall_length // (self.insul[0] + self.ver_rib_thick)
        x_resid = self.wall_length % (self.insul[0] + self.ver_rib_thick)
        if x_resid > self.insul[0]:
            x_resid = self.insul[0]

        if position:
            n = - self.insul[0]; m = - x_resid; l = - 1
        else:
            n = 0; m = 0; l = 1

        insul_list1 = self.insul_support_func(self.insul[0], self.insul[1], num_x_step, num_z_step, x_resid, z_resid, 0, 1, insul_type, n, m, l)
        insul_list2 = self.insul_support_func(self.insul[0], self.insul[1], num_x_step, num_z_step, x_resid, z_resid, 0, 2, insul_type, n, m, l)
        line_list = self.insul_support_func(self.insul[0], self.insul[1], num_x_step, num_z_step, x_resid, z_resid, 0, 3, insul_type, n, m, l)

        for insul1, insul2, line in zip(insul_list1, insul_list2, line_list):
            insul_fix_list.append(self.create_insul_group_fixture(insul1, insul2, line, num))
            num += 1
        return insul_fix_list    

    def create_hor_insulation(self, insul_type, num, position = False):
        insul_fix_list = []
        if self.wall_height <= 0:
            return insul_fix_list

        if self.wall_height >= self.insul[0]:
            temp = self.insul[0]
            self.insul[0] = self.insul[1]
            self.insul[1] = temp

        num_z_step = self.wall_height // (self.insul[0] + self.hor_rib_thick)
        z_resid = self.wall_height % (self.insul[0] + self.hor_rib_thick)
        if z_resid > self.insul[0]:
            z_resid = self.insul[0]

        num_x_step = self.wall_length // (self.insul[1] + self.ver_rib_thick)
        x_resid = self.wall_length % (self.insul[1] + self.ver_rib_thick)
        
        x_offset = 0
        if x_resid < self.insul[3]:
            x_offset = (self.wall_length - self.insul[1] * num_x_step - self.ver_rib_thick * (num_x_step - 1)) / 2  
        if x_resid > self.insul[1]:
            x_offset = (x_resid - self.insul[1]) / 2
            x_resid = self.insul[1]    
        if self.wall_length >= (self.insul[1] + self.ver_rib_thick) * num_x_step + self.insul[3]:
            x_resid = (self.wall_length - self.ver_rib_thick * num_x_step) / (num_x_step + 1) 
            if x_resid > self.insul[1]:
                x_resid = self.insul[1]
            self.insul[1] = x_resid

        if position:
            n = - self.insul[0]; m = - x_resid; l = - 1
        else:
            n = 0; m = 0; l = 1

        insul_list1 = self.insul_support_func(self.insul[1], self.insul[0], num_x_step, num_z_step, x_resid, z_resid, x_offset, 1, insul_type, n, m, l)
        insul_list2 = self.insul_support_func(self.insul[1], self.insul[0], num_x_step, num_z_step, x_resid, z_resid, x_offset, 2, insul_type, n, m, l)
        line_list = self.insul_support_func(self.insul[1], self.insul[0], num_x_step, num_z_step, x_resid, z_resid, x_offset, 3, insul_type, n, m, l)

        for insul1, insul2, line in zip(insul_list1, insul_list2, line_list):
            insul_fix_list.append(self.create_insul_group_fixture(insul1, insul2, line, num))
            num += 1
        return insul_fix_list    

    def insul_support_func(self, insul_width, insul_height, num_x_step, num_z_step, x_resid, z_resid, x_offset, type, insul_type, n=0, m=0, l=1):
        insul_list = []
        
        y_offset = 30 if insul_type else 0 
        insul_thick = self.insul[2] - 30 if insul_type else self.insul[2]

        if type == 1:
            insul1 = AllplanGeo.Polygon3D()
            insul1 += AllplanGeo.Point3D(0, insul_thick, 0)
            insul1 += AllplanGeo.Point3D(insul_width, insul_thick, 0)
            insul1 += AllplanGeo.Point3D(insul_width, insul_thick, insul_height)
            insul1 += AllplanGeo.Point3D(0, insul_thick, insul_height)
            insul1 += AllplanGeo.Point3D(0, insul_thick, 0)
        elif type == 2:
            insul1 = AllplanGeo.Polyhedron3D.CreateCuboid(insul_width, insul_thick, insul_height)
        else:
            point1 = AllplanGeo.Point3D(0, 0, 0)
            point2 = AllplanGeo.Point3D(0, insul_thick, 0)
            insul1 = AllplanGeo.Line3D(point1, point2)

        if type == 1:
            insul2 = AllplanGeo.Polygon3D()
            insul2 += AllplanGeo.Point3D(0, insul_thick, 0)
            insul2 += AllplanGeo.Point3D(insul_width, insul_thick, 0)
            insul2 += AllplanGeo.Point3D(insul_width, insul_thick, z_resid)
            insul2 += AllplanGeo.Point3D(0, insul_thick, z_resid)
            insul2 += AllplanGeo.Point3D(0, insul_thick, 0)
        elif type == 2:
            insul2 = AllplanGeo.Polyhedron3D.CreateCuboid(insul_width, insul_thick, z_resid)
        else:
            point1 = AllplanGeo.Point3D(0, 0, 0)
            point2 = AllplanGeo.Point3D(0, insul_thick, 0)
            insul2 = AllplanGeo.Line3D(point1, point2)

        if type == 1:
            insul3 = AllplanGeo.Polygon3D()
            insul3 += AllplanGeo.Point3D(0, insul_thick, 0)
            insul3 += AllplanGeo.Point3D(x_resid, insul_thick, 0)
            insul3 += AllplanGeo.Point3D(x_resid, insul_thick, insul_height)
            insul3 += AllplanGeo.Point3D(0, insul_thick, insul_height)
            insul3 += AllplanGeo.Point3D(0, insul_thick, 0)
        elif type == 2:
            insul3 = AllplanGeo.Polyhedron3D.CreateCuboid(x_resid, insul_thick, insul_height)
        else:
            point1 = AllplanGeo.Point3D(0, 0, 0)
            point2 = AllplanGeo.Point3D(0, insul_thick, 0)
            insul3 = AllplanGeo.Line3D(point1, point2)

        if type == 1:
            insul4 = AllplanGeo.Polygon3D()
            insul4 += AllplanGeo.Point3D(0, insul_thick, 0)
            insul4 += AllplanGeo.Point3D(x_resid, insul_thick, 0)
            insul4 += AllplanGeo.Point3D(x_resid, insul_thick, z_resid)
            insul4 += AllplanGeo.Point3D(0, insul_thick, z_resid)
            insul4 += AllplanGeo.Point3D(0, insul_thick, 0)
        elif type == 2:
            insul4 = AllplanGeo.Polyhedron3D.CreateCuboid(x_resid, insul_thick, z_resid)
        else:
            point1 = AllplanGeo.Point3D(0, 0, 0)
            point2 = AllplanGeo.Point3D(0, insul_thick, 0)
            insul4 = AllplanGeo.Line3D(point1, point2)

        for i in range(0, int(num_x_step)):
            for j in range(0, int(num_z_step)):                
                insul_i = AllplanGeo.Move(insul1, AllplanGeo.Vector3D(self.start_point +  l * i * (insul_width + self.ver_rib_thick) + n + x_offset,
                                                                      y_offset, self.z_start_point + j * (insul_height + self.hor_rib_thick)))
                insul_list.append(insul_i)      
            insul_i = AllplanGeo.Move(insul2, AllplanGeo.Vector3D(self.start_point + l * i * (insul_width + self.ver_rib_thick) + n + x_offset,
                                                                  y_offset, self.z_start_point + num_z_step * (insul_height + self.hor_rib_thick)))
            insul_list.append(insul_i)

        if x_resid >= self.insul[3] and z_resid >= self.insul[3]:
            for i in range(0, int(num_z_step)):
                insul_i = AllplanGeo.Move(insul3, AllplanGeo.Vector3D(self.start_point + l * num_x_step * (insul_width + self.ver_rib_thick) + m + x_offset,
                                                                      y_offset, self.z_start_point + i * (insul_height + self.hor_rib_thick)))
                insul_list.append(insul_i)   
            insul_i = AllplanGeo.Move(insul4, AllplanGeo.Vector3D(self.start_point + l * num_x_step * (insul_width + self.ver_rib_thick) + m + x_offset,
                                                                  y_offset, self.z_start_point + num_z_step * (insul_height + self.hor_rib_thick)))
            insul_list.append(insul_i)
        return insul_list
   
    def create_insul_group_fixture(self, insul1, insul2, line, num):
        attr_list = []
        attr_set_list = []
        
        location = AllplanGeo.Point3D(0, 0, 0)
        symbol_prop = AllplanBasisElements.Symbol3DProperties()
        symbol_prop.SymbolID = 1
        symbol_prop.Height = 1
        symbol_prop.Width = 1
        symbol_list = [AllplanBasisElements.Symbol3DElement(self.com_prop, symbol_prop, location)]

        slide_sym_prop = AllplanPrecast.FixtureSlideProperties()
        slide_sym_prop.ViewType = AllplanPrecast.FixtureSlideViewType.eCONNECTION_POINT
        slide_list = [AllplanPrecast.FixtureSlideElement(slide_sym_prop, symbol_list)]      
              
        fix_macro_grp_prop = AllplanPrecast.FixtureProperties()
        fix_macro_grp_prop.Type = AllplanPrecast.MacroType.eGroup_Fixture 
        fix_macro_grp = AllplanPrecast.FixtureElement(fix_macro_grp_prop, slide_list)
        fix_macro_grp.SetHash(hashlib.sha224(str(fix_macro_grp).encode('utf-8')).hexdigest())
         
        fixture_grp_pl_prop = AllplanPrecast.FixturePlacementProperties()
        fixture_grp_pl_prop.Name = "УТ" + str(num) 
        fixtureGrp = AllplanPrecast.FixturePlacementElement(self.com_prop, fixture_grp_pl_prop, fix_macro_grp)
   
        attr_list.append(AllplanBaseElements.AttributeInteger(1013, 0))
        attr_set_list.append(AllplanBaseElements.AttributeSet(attr_list))
        attributes = AllplanBaseElements.Attributes(attr_set_list)
       
        group_list = [fixtureGrp]
        group_list.append(self.create_fir_insul_fixture(insul1, num))
        group_list.append(self.create_sec_insul_fixture(insul2, line, num))

        fixture_grp_prop = AllplanPrecast.FixtureGroupProperties()
        fixture_grp_prop.Name = "УТ"
        group = AllplanPrecast.FixtureGroupElement(fixture_grp_prop, group_list)
        group.SetAttributes(attributes)
        return group

    def create_fir_insul_fixture(self, insul, num):
        attr_list = []
        attr_set_list = []
        insul_slides = []

        insul_list = [AllplanBasisElements.ModelElement3D(self.com_prop, insul)]
        
        insul_slide_prop_3d = AllplanPrecast.FixtureSlideProperties()
        insul_slide_prop_3d.ViewType = AllplanPrecast.FixtureSlideViewType.e3D_VIEW
        insul_slides.append(AllplanPrecast.FixtureSlideElement(insul_slide_prop_3d, insul_list))    
            
        insul_fixture_prop = AllplanPrecast.FixtureProperties()
        insul_fixture_prop.Type = AllplanPrecast.MacroType.ePlane_Fixture
        insul_fixture_prop.Name = "УТ" + str(num)      
        insul_fixture = AllplanPrecast.FixtureElement(insul_fixture_prop, insul_slides)
        insul_fixture.SetHash(hashlib.sha224(str(insul_fixture).encode('utf-8')).hexdigest())

        insul_fixture_place_prop = AllplanPrecast.FixturePlacementProperties()
        insul_fixture_place_prop.Name = "УТ"
        insul_fixture_place_prop.ConnectionToAIACatalog = True
        
        attr_list.append(AllplanBaseElements.AttributeString(1332, "УТ_пов"))
        attr_list.append(AllplanBaseElements.AttributeInteger(1013, 50))
        attr_set_list.append(AllplanBaseElements.AttributeSet(attr_list))
        attributes = AllplanBaseElements.Attributes(attr_set_list)
        
        insul_fixture_place = AllplanPrecast.FixturePlacementElement(self.com_prop, insul_fixture_place_prop, insul_fixture)
        insul_fixture_place.SetAttributes(attributes)
        return insul_fixture_place

    def create_sec_insul_fixture(self, insul, line, num):    
        insul_slides = []
        attr_list = []
        attr_set_list = []
        
        line_list = [AllplanBasisElements.ModelElement3D(self.com_prop, line)]
        insul_slide_3d = [AllplanBasisElements.ModelElement3D(self.com_prop1, insul)]

        insul_slide_prop_3d = AllplanPrecast.FixtureSlideProperties()
        insul_slide_prop_3d.ViewType = AllplanPrecast.FixtureSlideViewType.e3D_VIEW
        insul_slides.append(AllplanPrecast.FixtureSlideElement(insul_slide_prop_3d, line_list)) 
        
        insul_slide_prop_3d_out_vol = AllplanPrecast.FixtureSlideProperties()
        insul_slide_prop_3d_out_vol.ViewType = AllplanPrecast.FixtureSlideViewType.e3D_VIEW_OUTLINE_VOLUME
        insul_slides.append(AllplanPrecast.FixtureSlideElement(insul_slide_prop_3d_out_vol, insul_slide_3d))    

        insul_fixture_prop = AllplanPrecast.FixtureProperties()
        insul_fixture_prop.Type = AllplanPrecast.MacroType.eLine_Fixture
        insul_fixture_prop.SubType = AllplanPrecast.MacroSubType.ePrefabModeller
        insul_fixture_prop.Name = "XXX" + str(num)   
        insul_fixture = AllplanPrecast.FixtureElement(insul_fixture_prop, insul_slides)
        insul_fixture.SetHash(hashlib.sha224(str(insul_fixture).encode('utf-8')).hexdigest())

        insul_fixture_place_prop = AllplanPrecast.FixturePlacementProperties()
        insul_fixture_place_prop.Name = "XXX"
        insul_fixture_place_prop.OutlineType = AllplanPrecast.OutlineType.eBUILTIN_OUTLINE_TYPE_MINUS
        insul_fixture_place_prop.OutlineTypeInGroup = AllplanPrecast.OutlineTypeInGroup.eBUILTIN_OUTLINE_TYPE_IN_GROUP_MINUS
        insul_fixture_place_prop.OutlineShape = AllplanPrecast.OutlineShape.eBUILTIN_OUTLINE_SHAPE_SYMBOL

        attr_set_list.append(AllplanBaseElements.AttributeSet(attr_list))
        attributes = AllplanBaseElements.Attributes(attr_set_list)
        
        insul_fixture_place = AllplanPrecast.FixturePlacementElement(self.com_prop, insul_fixture_place_prop, insul_fixture)
        insul_fixture_place.SetAttributes(attributes)
        return insul_fixture_place

    @staticmethod
    def create_fill(fill_length, fill_thick, fill_start_point, create_filling):
        if fill_length <= 0 or not create_filling:
            return None

        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()
        com_prop.Layer = 3717
        color = AllplanBasisElements.ARGB (180, 180, 180, 0)
        props = AllplanBasisElements.FillingProperties()
        props.FirstColor = color

        polygon = AllplanGeo.Polygon2D()
        polygon += AllplanGeo.Point2D(0, 0)
        polygon += AllplanGeo.Point2D(fill_length, 0)
        polygon += AllplanGeo.Point2D(fill_length, fill_thick)
        polygon += AllplanGeo.Point2D(fill_length, fill_thick)
        polygon += AllplanGeo.Point2D(0, fill_thick)
        polygon += AllplanGeo.Point2D(0, 0)
        
        polygon = AllplanGeo.Move(polygon, AllplanGeo.Vector2D(fill_start_point, 0))
        return AllplanBasisElements.FillingElement(com_prop, props, polygon)
 

    def create_ribb_reinf(self, orient_params, wall_thick):
        library_ele_list = []
        #num_z_step = self.wall_height // (self.insul[1] + self.hor_rib_thick)

        placement_mat = RotationAngles(0, 0, orient_params[3]).get_rotation_matrix()

        placement_mat.SetTranslation(AllplanGeo.Vector3D(1000 * m.cos(m.radians(orient_params[3])) + orient_params[1] * m.sin(m.radians(orient_params[3])), 1000 * m.sin(m.radians(orient_params[3])) + orient_params[2] * m.cos(m.radians(orient_params[3])), self.wall_height))

        if wall_thick == 160:
            lib_ele_prop = AllplanBasisElements.LibraryElementProperties(AllplanSettings.AllplanPaths.GetStdPath(), 'Каркасы вертикальные (стены)', 'К-6(10/6)15', AllplanBasisElements.LibraryElementType.eFixture, placement_mat)
        else:
            return library_ele_list

        library_ele_list.append(AllplanBasisElements.LibraryElement(lib_ele_prop))
        return library_ele_list




















    #def create_pylon_reinf(self):
    #    placement_mat = RotationAngles(0, 0, self.wall_orient[3]).get_rotation_matrix()

    #    if self.rotate_pylon:
    #        placement_mat.SetTranslation(AllplanGeo.Vector3D(self.pylon_posit * m.cos(m.radians(self.wall_orient[3])) + self.wall_orient[1] - self.wall_thick / 2 * m.sin(m.radians(self.wall_orient[3])), self.pylon_posit * m.sin(m.radians(self.wall_orient[3])) + self.wall_orient[2] + self.wall_thick / 2 * m.cos(m.radians(self.wall_orient[3])), self.wall_height + 60))
    #    else:
    #        placement_mat.SetTranslation(AllplanGeo.Vector3D(self.pylon_posit * m.cos(m.radians(self.wall_orient[3])) + self.wall_orient[1] - self.wall_thick / 2 * m.sin(m.radians(self.wall_orient[3])), self.pylon_posit * m.sin(m.radians(self.wall_orient[3])) + self.wall_orient[2] + self.wall_thick / 2 * m.cos(m.radians(self.wall_orient[3])), self.wall_height + 60))

    #    if self.wall_thick == 160:
    #        lib_ele_prop = AllplanBasisElements.LibraryElementProperties(AllplanSettings.AllplanPaths.GetStdPath(), 'ПК (стены)', '1ПК-33/16',
    #                                                                    AllplanBasisElements.LibraryElementType.eFixture, placement_mat)
    #    else:
    #        return self.library_ele_list

    #    self.library_ele_list.append(AllplanBasisElements.LibraryElement(lib_ele_prop))
    #    return self.library_ele_list

    #def create_pylon_fixture(self):
        
    #    for z_posit in [230, 945, 1695, 2445, 3185]:
    #        placement_mat = RotationAngles(0, 0, 0).get_rotation_matrix()
    #        placement_mat.SetTranslation(AllplanGeo.Vector3D(0, 0, z_posit))

    #    #if self.rotate_pylon:
    #    #    placement_mat.SetTranslation(AllplanGeo.Vector3D(self.pylon_posit, self.wall_thick / 2, self.wall_height + 105))
    #    #else:
    #    #    placement_mat.SetTranslation(AllplanGeo.Vector3D(self.pylon_posit, self.wall_thick / 2, self.wall_height - 95))

    #        if self.wall_thick == 160:
    #            lib_ele_prop = AllplanBasisElements.LibraryElementProperties(AllplanSettings.AllplanPaths.GetStdPath(), 'Закладные детали (т.160)', 'ЗД-9п-1',
    #                                                                        AllplanBasisElements.LibraryElementType.eFixture, placement_mat)
    #            self.library_ele_list.append(AllplanBasisElements.LibraryElement(lib_ele_prop))
    #        else:
    #            return self.library_ele_list

        
    #    return self.library_ele_list


        #def create_cent_pylon_reinf(self):
        #placement_mat = RotationAngles(0, 0, self.wall_orient[3]).get_rotation_matrix()
        
        #if self.rotate_pylon:
        #    placement_mat.SetTranslation(AllplanGeo.Vector3D(self.cent_pylon_posit * m.cos(m.radians(self.wall_orient[3])) + self.wall_orient[1] - self.wall_thick / 2 * m.sin(m.radians(self.wall_orient[3])), self.cent_pylon_posit * m.sin(m.radians(self.wall_orient[3])) + self.wall_orient[2] + self.wall_thick / 2 * m.cos(m.radians(self.wall_orient[3])), self.wall_height + 60))
        #else:
        #    placement_mat.SetTranslation(AllplanGeo.Vector3D(self.cent_pylon_posit * m.cos(m.radians(self.wall_orient[3])) + self.wall_orient[1] - self.wall_thick / 2 * m.sin(m.radians(self.wall_orient[3])), self.cent_pylon_posit * m.sin(m.radians(self.wall_orient[3])) + self.wall_orient[2] + self.wall_thick / 2 * m.cos(m.radians(self.wall_orient[3])), self.wall_height + 60))

        #if self.cent_pylon_length == 500 and self.cent_pylon_thick == 160:
        #    lib_ele_prop = AllplanBasisElements.LibraryElementProperties(AllplanSettings.AllplanPaths.GetStdPath(), 'ПК (стены)', '1ПК-33/16т',
        #                                                                AllplanBasisElements.LibraryElementType.eFixture, placement_mat)
        #elif self.cent_pylon_length == 1010 and self.cent_pylon_thick == 160:
        #    lib_ele_prop = AllplanBasisElements.LibraryElementProperties(AllplanSettings.AllplanPaths.GetStdPath(), 'ПК (стены)', '2ПК-33/16т',
        #                                                                AllplanBasisElements.LibraryElementType.eFixture, placement_mat)
        #else:
        #    return self.library_ele_list
        #self.library_ele_list.append(AllplanBasisElements.LibraryElement(lib_ele_prop))
        #return self.library_ele_list