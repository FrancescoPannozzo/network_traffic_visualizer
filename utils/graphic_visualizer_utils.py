" Graphic visualizer utils"

from datetime import datetime


def get_test_duration(start_time):
    end_time = datetime.now()
    duration = end_time - start_time
    
    return f"Test duration:{duration}"