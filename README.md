#  Tensor-Tracer

## 功能简介:
自定以的tracer, 为了跟踪神经网络代码的运行轨迹, 同时列出不同张量的shape,size等的权重变化信息.

打印出的效果如下:
```
2621--------> [ call function ListDataset#__getitem__ ]
------ print self ------
[var:] img_files [list#length:117264]
[var:] label_files [list#length:117264]
[var:] img_size [float or int#value:416]
[var:] max_objects [float or int#value:100]
[var:] augment [bool#value:"True"]
[var:] multiscale [bool#value:"True"]
[var:] normalized_labels [bool#value:"True"]
[var:] min_size [float or int#value:320]
[var:] max_size [float or int#value:512]
[var:] batch_count [float or int#value:0]
[arg:] index [float or int#value:57956]
2621          |line 77|        def __getitem__(self, index):
2622          |line 83|            img_path = self.img_files[index % len(self.img_files)].rstrip()
2623          |line 86|            img = transforms.ToTensor()(Image.open(img_path).convert('RGB'))
2624          |line 89|            if len(img.shape) != 3:
2625          |line 93|            _, h, w = img.shape
2626          |line 94|            h_factor, w_factor = (h, w) if self.normalized_labels else (1, 1)
2627          |line 96|            img, pad = pad_to_square(img, 0)
------------/home/tst/PyTorch-YOLOv3/utils/datasets.py------------
2628------------> [ call function pad_to_square ]
[arg:] img [torch.Tensor#size:torch.Size([3, 483, 640])]
[arg:] pad_value [float or int#value:0]
2628              |line 15|    def pad_to_square(img, pad_value):
2629              |line 16|        c, h, w = img.shape
2630              |line 17|        dim_diff = np.abs(h - w)
2631              |line 19|        pad1, pad2 = dim_diff // 2, dim_diff - dim_diff // 2
2632              |line 21|        pad = (0, 0, pad1, pad2) if h <= w else (pad1, pad2, 0, 0)
2633              |line 23|        img = F.pad(img, pad, "constant", value=pad_value)
2634              |line 25|        return img, pad
2635<------------ [ exit function pad_to_square ]
```


## 安装
```
python setup.py install
```

## 使用:
```
  ttracer 目标文件.py  目标文件的参数
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
```
