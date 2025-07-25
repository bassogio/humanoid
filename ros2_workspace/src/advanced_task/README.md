# advanced_task

## Overview

This ROS 2 package streams camera images and performs real-time object detection using yolo11n.  
You can choose to run either the **rgb_publisher** node (for raw RGB images) or the **llm_integration** node (for annotated images and detection metadata).

---

## Package Contents

- `RGB_publisher.py`: Publishes raw RGB images from a selected camera.
- `LLM_integration.py`: Publishes annotated images with yolo11n detections, detection metadata, and moving direction.
- `detect_cameras.py`: Utility script to list available camera indices and names.

---

## Requirements

- ROS2 
- Python 3.8+
- OpenCV
- cv_bridge
- ultralytics (yolo11n)
- torch

Install dependencies:
```bash
pip install opencv-python ultralytics torch
sudo apt install ros-<distro>-cv-bridge
```

---

## Parameters

### rgb_publisher (RGB_publisher.py)
| Name               | Default            | Description                             |
| ------------------ | ------------------ | --------------------------------------- |
| `publisher_topic`  | /camera/image_raw  | Topic to publish RGB image              |
| `camera_index`     | 0                  | The index of the camera                 |
| `publish_rate`     | 10                 | Rate in Hz to publish data on ROS topic |

### llm_integration (LLM_integration.py)
| Name                       | Default                | Description                                     |
| -------------------------- | ---------------------- | ----------------------------------------------- |
| `publisher_raw_topic`      | /camera/image_raw      | Topic to publish raw RGB image                  |
| `publisher_detected_topic` | /camera/detected_target| Topic to publish annotated image with detection |
| `publisher_moving_direction_topic` | /robotAction   | Topic to publish moving direction commands      |
| `publisher_meta_topic`     | /detections            | Topic to publish detection metadata (JSON)      |
| `camera_index`             | 0                      | The index of the camera                         |
| `publish_rate`             | 30                     | Rate in Hz to publish data on ROS topic         |
| `target_class`             | person                 | The class to detect (can be updated dynamically)|

---

## How to Build

Open a terminal, navigate to your workspace root and run:

```bash
colcon build
source install/setup.bash
```

---

## Camera Selection

If you are unsure which camera index to use, run:

```bash
cd ros2_workspace/src/advanced_task/advanced_task/
python3 detect_cameras.py
```

This will list all connected cameras and their indices.  
Example output:
```bash
Available cameras:
  Index 0: C922 Pro Stream Webcam
  Index 2: Microsoft® LifeCam HD-3000: Mi
```
Update the `camera_index` parameter in your launch or run command as needed.

---

## How to Run

Choose **one** of the following nodes to run:

### To see only the raw RGB image:
```bash
ros2 run advanced_task rgb_publisher
```
Override parameters if needed:
```bash
ros2 run advanced_task rgb_publisher --ros-args -p camera_index:=2 -p publish_rate:=5
```

### To see RGB image with LLM (yolo11n) detection:
```bash
ros2 run advanced_task llm_integration
```
Override parameters if needed:
```bash
ros2 run advanced_task llm_integration --ros-args -p target_class:=bowl
```

#### Dynamically Change Target Class

You can update the target class (e.g., from "bottle" to "bowl") at runtime by publishing to `/target_class`:

```bash
ros2 topic pub -1 /target_class std_msgs/String "data: 'bowl'"
```
- The node will immediately start detecting and annotating the new class.

***The video below demonstrates how executing the following command results in the system updating the target to the bowl.***

https://github.com/user-attachments/assets/ffc8d6e7-f165-4394-ad4e-74a5a235f463


---

### Select a Specific Target Instance

If multiple objects of the target class are detected, you can select which one to follow by publishing its ID to `/selected_target_id`:

```bash
ros2 topic pub -1 /selected_target_id std_msgs/String "data: '1'"
```
- The ID corresponds to the label shown in the annotated image (e.g., "bottle #1").
- If only one target is detected, selection is reset and the node will wait for a new selection when multiple targets appear again.

***The video below demonstrates how the "Moving Direction" is dynamically updated based on the selected object to track.
It also shows the system’s handling of multiple recognized objects that belong to the same category.***

https://github.com/user-attachments/assets/f2b2337b-041d-49c0-8768-fa8f78494931

***Here is another demonstration:***

https://github.com/user-attachments/assets/73ea6ce2-731a-4dfb-98f5-560d70480b23


---

## Topics Published & Subscribed

**Published:**
- `/camera/image_raw`: Raw RGB images (`sensor_msgs/Image`)
- `/camera/detected_target`: Annotated images with YOLO detections (`sensor_msgs/Image`)
- `/detections`: Detection metadata as JSON (`std_msgs/String`)
- `/robotAction`: Moving direction for robot (`std_msgs/String`)

**Subscribed:**
- `/target_class`: Dynamically update which class to detect (`std_msgs/String`)
- `/selected_target_id`: Select which detected instance to follow (`std_msgs/String`)

---

**Note:**  
- Use the `-1` flag with `ros2 topic pub` to publish only once.
- Make sure your node is running and subscribing to these topics before publishing.

---

## Troubleshooting

- If you see "Could not open camera", check your camera index and permissions.


