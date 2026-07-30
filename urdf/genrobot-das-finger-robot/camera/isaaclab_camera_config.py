"""Generated camera parameters for Isaac Lab / Isaac Sim.

Isaac Lab's CameraCfg creates the camera prim and ideal intrinsics. RTX lens
distortion is then applied through Isaac Sim's native OpenCV lens schema API.
"""

from isaaclab.sensors import CameraCfg
import isaaclab.sim as sim_utils

WIDTH = 1600
HEIGHT = 1300
K = [505.3665667809046, 0.0, 795.124005940977, 0.0, 505.9970483418306, 655.966646695526, 0.0, 0.0, 1.0]  # row-major 3x3

CAMERA_CFG = CameraCfg(
    prim_path="/World/envs/env_.*/Camera",
    width=WIDTH,
    height=HEIGHT,
    data_types=["rgb"],
    spawn=sim_utils.PinholeCameraCfg.from_intrinsic_matrix(
        intrinsic_matrix=K,
        width=WIDTH,
        height=HEIGHT,
        clipping_range=(0.01, 100.0),
        f_stop=0.0,
    ),
)

# Native OpenCV distortion coefficient order used by Isaac Sim 5.x:
# pinhole: [k1,k2,p1,p2,k3,k4,k5,k6,s1,s2,s3,s4]
ISAAC_OPENCV_PINHOLE = [-1.8324856404608678, 1.158612635778741, -0.0027529834905140986, -0.0006750739819676449, -0.1362592954741474, -1.5688085694030354, 0.696932209920747, 0.10891260295540811, 0.0, 0.0, 0.0, 0.0]
# fisheye: [k1,k2,k3,k4]
ISAAC_OPENCV_FISHEYE = [0.05246115523491198, -0.004467628809391041, 0.0018344295518293327, -0.0003957181963575988]
PREFERRED_MODEL = 'opencv_fisheye'
PARAMETER_SOURCE = 'recorded_double_sphere_converted_to_opencv_fisheye'


def apply_native_distortion(camera):
    """Call after the isaacsim.sensors.camera.Camera object is initialized.

    For Isaac Sim 6.x, author the equivalent
    OmniLensDistortionOpenCvPinholeAPI or OmniLensDistortionOpenCvFisheyeAPI
    schema on the RTX camera prim; the numeric coefficient order is unchanged.
    """
    fx, fy, cx, cy = K[0], K[4], K[2], K[5]
    if PREFERRED_MODEL == "opencv_fisheye":
        camera.set_opencv_fisheye_properties(
            cx=cx, cy=cy, fx=fx, fy=fy, fisheye=ISAAC_OPENCV_FISHEYE
        )
    else:
        camera.set_opencv_pinhole_properties(
            cx=cx, cy=cy, fx=fx, fy=fy, pinhole=ISAAC_OPENCV_PINHOLE
        )
