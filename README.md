python安装 bleak库、keyboard库
python -m pip install bleak keyboard

直接运行，在键盘上按wasd 是上下左右，j是A   k是B   g是select  h是start
蓝牙发送的数据格式是
BB 00 XX EE
其中XX的每个位代表一个按钮按下与否，1为按下，0为松开
XX的 高位到低位代表
8bit 7bit 6bit 5bit   4bit     3bit    2bit   1bit
右    左   下    上   start   select     B      A
