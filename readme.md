# Road Detection CNN

## Installation

1. Clone the repository:

    ```Shell
    git clone https://github.com/silvadirceu/Road_detection_CNN.git

    cd road-detection-system
    ```

2. Set up environment variables:
    * Create a .env file in the project root.
    * Add the following variables:
    ```Shell
    IS_DEV=1  # Set to 0 for production mode
    CATEGORIES=clean dirty potholes
    TRAIN_PATH=/path/to/training_data
    TEST_PATH=/path/to/testing_data
    ```
 
 ## How to run

1. Locally without docker
    ```Shell
    pip install -r requirements.txt

    python api/main.py
    ```

2. Docker container
    ```Shell
    docker build -t road_detection_cnn .

    docker run -p 8000:8000 road_detection_cnn 
    ```

