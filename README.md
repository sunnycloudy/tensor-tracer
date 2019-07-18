#  Tensor-Tracer

## 功能简介:
自定义的tracer, 为了跟踪神经网络代码的运行轨迹, 同时列出不同张量的shape,size等的权重变化信息.

打印出的效果如下:
```
------------/home/tst/PyTorch-YOLOv3/train.py------------
train.py            :    1  |[ call function <module> ]
[var:] __name__             [str#value:"train"]
[arg:] __doc__              [type not included:]<class 'NoneType'><id:9098912>
[var:] __package__          [str#value:""]
[arg:] __loader__           [type not included:]<class '_frozen_importlib_external.SourceFileLoader'><id:139867071663800>
[arg:] __spec__             [type not included:]<class '_frozen_importlib.ModuleSpec'><id:139867071663856>
[var:] __file__             [str#value:"/home/tst/PyTorch-YOLOv3/train.py"]
[var:] __cached__           [str#value:"/home/tst/PyTorch-YOLOv3/__pycache__/train.cpython-37.pyc"]
[var:] __builtins__         [dict#length:153]
train.py            :    1  |L    1|    from __future__ import division
train.py            :    2  |L    1|    from __future__ import division
train.py            :    3  |L    3|    from models import *
------------/home/tst/PyTorch-YOLOv3/models.py------------
models.py           :    4  |[ call function <module> ]
[var:] __name__             [str#value:"models"]
[arg:] __doc__              [type not included:]<class 'NoneType'><id:9098912>
[var:] __package__          [str#value:""]
[arg:] __loader__           [type not included:]<class '_frozen_importlib_external.SourceFileLoader'><id:139867071362552>
[arg:] __spec__             [type not included:]<class '_frozen_importlib.ModuleSpec'><id:139867071362608>
[var:] __file__             [str#value:"/home/tst/PyTorch-YOLOv3/models.py"]
[var:] __cached__           [str#value:"/home/tst/PyTorch-YOLOv3/__pycache__/models.cpython-37.pyc"]
[var:] __builtins__         [dict#length:153]
models.py           :    4  |L    1|    from __future__ import division
models.py           :    5  |L    1|    from __future__ import division
models.py           :    6  |L    3|    import torch
models.py           :    7  |L    4|    import torch.nn as nn
models.py           :    8  |L    5|    import torch.nn.functional as F
models.py           :    9  |L    6|    from torch.autograd import Variable
models.py           :   10  |L    7|    import numpy as np
models.py           :   11  |L    9|    from utils.parse_config import *
```

## 安装:
```
python setup.py install
```

## 使用:
```
  ttracer 目标文件.py  目标文件的参数
```

## 注意:
目标文件应该是通过这种方式启动
```
if __name__ == "__main__":
  main()
```

## 配置:
在目标的py文件目录增加一个tt_config.py
例如:

```
target_files=["models.py", "utils/datasets.py"]  #代表tracer会跟踪的其他目标文件.
maxline=20000                                    #代表tracer会跟踪的行数, 默认是10000行.
ignore_lines = {                                 #代表会忽略的文件中的行, 每个函数的call内只会打印一次.
  "utils/datasets.py": [65,66]
}
ignore_functions = ["<listcomp>", "<dictcomp>"]  #代表会忽略的函数的调用, 一次都不打印
trace_width = 60                                 #代表了代码的自动换行的触发长度
```
