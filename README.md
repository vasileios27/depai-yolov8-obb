# DeployAI Object Detection

This repository contains a deep learning model for detecting objects from very high resolution optical remote sensing images using `YOLOv8 Oriented Bounding Box`.

## Key features

The model allows detecting the following objects

```python
{
    "plane": 0,
    "ship": 1,
    "storage-tank": 2,
    "baseball-diamond": 3,
    "tennis-court": 4,
    "basketball-court": 5,
    "ground-track-field": 6,
    "harbor": 7,
    "bridge": 8,
    "large-vehicle": 9,
    "small-vehicle": 10,
    "helicopter": 11,
    "roundabout": 12,
    "soccer-ball-field": 13,
    "swimming-pool": 14,
    "container-crane": 15,
    "airport": 16,
    "helipad": 17,
}
```

## Input Format

The input image should be of size $1024\times1024\times3$, which means RGB images. The image extension can be `tif, png, and jpg`.

## Output Format

The output is a text file that contains one or multiple lines. Each line is associated with one detected object. A line starts with the class ID, the coordinates of the bounding box in as floats and the final float number is the confidence of the model for this detected object. The following is an example of an output file

```powershell
10 0.769302 0.0571918 0.771534 0.0672572 0.792736 0.0625548 0.790504 0.0524893 0.76106
10 0.616684 0.486967 0.617148 0.478474 0.597924 0.477423 0.59746 0.485916 0.750721
10 0.510295 0.481979 0.510747 0.471428 0.490472 0.470558 0.490019 0.481109 0.548859
10 0.522158 0.0857164 0.524665 0.095236 0.546002 0.0896183 0.543495 0.0800987 0.545464
10 0.132021 0.358989 0.143523 0.356336 0.138069 0.332698 0.126568 0.335351 0.537943
9 0.570139 0.719797 0.570226 0.732347 0.604308 0.732111 0.604221 0.719561 0.327334
10 0.930733 0.603296 0.941956 0.603665 0.94258 0.584695 0.931358 0.584326 0.317335
10 0.283544 0.659585 0.294072 0.659736 0.294374 0.638583 0.283846 0.638433 0.301854
10 0.792477 0.0173265 0.800817 0.0147654 0.79538 -0.00294156 0.78704 -0.000380462 0.300901
10 0.808204 0.0153187 0.815899 0.0122031 0.809846 -0.00274596 0.802151 0.000369608 0.294774
10 0.890847 0.281562 0.891716 0.273191 0.875498 0.271507 0.874628 0.279878 0.283491
10 0.989942 0.247576 0.999541 0.251096 1.00361 0.240008 0.994008 0.236487 0.27634
```

> [!IMPORTANT]  
> If no objects are detected for an image, no output file is produced.

## Repository Content

```markdown
.
├── .github/
│ └── workflows/
│     └── build-test-image.yaml
├── README.md
├── Dockerfile
├── model.proto (Ptorobuf v3 specs)
├── requirements.txt
├── serve.py (gRPC service)
├── .gitignore
├── .dockerignore
├── .pylintrc
└── app/ (DL model)
    ├── init.py
    ├── config.py
    ├── utils.py
    ├── inference.py
    └── weights/
        └── best.pt
```

## Local Development

- In a terminal, clone the repository

```powershell
git clone https://github.com/AlbughdadiM/depai-yolov8-obb.git
```

- Go to the repository directory

```powershell
cd depai-yolov8-obb
```

- If the files `model_pb2_grpc.py` and `model_pb2.py` are not there, generate them using

```powershell
python3.10 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. model.proto
```

- Build the docker image

```powershell
docker build . -t object-detection:v0.1
```

- Create a container from the built image

```powershell
docker run --name=test -v ./test-data:/data -p 8061:8061 object-detection:v0.1
```

- Run the pytest

```powershell
pytest test_image_processor.py
```

## Container Registry

- Generate a personal access token: Github account settings > Developer settings > Personal access tokens (classic). Generate a token with the `read:package` scope.

- In a terminal, login to container registry using

```powershell
docker login ghcr.io -u USERNAME -p PAT 
```

- Pull the image
  
```powershell
docker pull ghcr.io/albughdadim/depai-yolov8-obb:v0.1
```

- Create a container

```powershell
docker run --name=test -p 8061:8061 ghcr.io/albughdadim/depai-yolov8-obb:v0.1
```

## How TO Use Example

```python
import grpc
import model_pb2
import model_pb2_grpc


def run():
    channel = grpc.insecure_channel("localhost:8061")
    stub = model_pb2_grpc.ImageProcessorStub(channel)
    # As we can see, the model accepts multiple images in a list
    response = stub.ProcessImage(
        model_pb2.ImageRequest(  # pylint: disable=E1101
            input_image_paths=[
                "/data/patch_250.tif",
                "/data/patch_420.tif",
            ]
        )
    )
    print("Output Result Path: " + response.entries[0].result_path)
    print("Output Result Path: " + response.entries[1].result_path)


if __name__ == "__main__":
    run()
```

This is a list that has the same length of the input one. In each element of the list, there is a dictinary with three keys:

- `image_path`: Input image path.
- `processed`: Boolean to indicate if an image is procssed or not.
- `result_path`: Output txt file containing bounding boxes of detected objects.
