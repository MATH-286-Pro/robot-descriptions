# Instructions

## Other Open Source Robot Description Repo
- [Google Deepmind XML files](https://github.com/google-deepmind/mujoco_menagerie/tree/main)

## Rules when creating .urdf
> **Physics**  
> DO NOT USE ZERO MASS OR ZERO INERTIA LINK  
> otherwise IsaacSim wil automaticlly add some mass and inertia when importing the .urdf files  

> **Joint**  
> Use dont_collapse="true" if you have fixed joint  
> Otherwise the fixed child link will become a sub-tree of parent link in **IsaacSim**    
```xml
  <joint name="joint1" type="fixed" dont_collapse="true">
    <axis xyz="1 0 0"/>
    <origin rpy="0 0 0" xyz="0 0 0"/>
    <parent link="link1"/>
    <child link="link2"/>
  </joint>
```

> **Material**  
> If you want you link to preserve coclor when imported to **IsaacSim**  
> Define the material color at the beginning of the .urdf file  
> Instead of define the material color in the link
```xml
# use this
  <material name="orange">
    <color rgba="1 0.27 0.0 1" />
  </material>

  <link name="vx300s_left_finger_link">
    <visual>
      <material name="orange"/>
    </visual>
  </link>

# instead of this
  <link name="vx300s_left_finger_link">
    <visual>
      <material name="orange">
        <color rgba="1.0 0.27 0.0 1.0"/>
      </material>
    </visual>
  </link>
```