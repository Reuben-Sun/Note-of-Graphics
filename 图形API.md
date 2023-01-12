# 图形API

## DX12

### 开始

安装[PIX](https://devblogs.microsoft.com/pix/download/)

安装Visual Studio 2019

### Windows应用程序

Windows应用程序使用事件驱动（详情可以去看WPF）

Windows应用程序的入口点是`WinMain`函数，主程序会创建一个窗口，并进入消息循环，检索处理操作系统发来的消息，并对其进行相应

当接收到`WM_QUIT`消息时（比如用户关闭窗口），会退出消息循环，应用程序即将结束，`WinMain`函数返回

### COM

#### 为什么要使用COM

> 我们在编写C++时，经常会生成dll文件，这是一种动态库，保存了许多通用的数据和函数，运行时软件可以通过函数指针的方式导出dll的函数，从而实现运行时动态链接
>
> 当我们在同一操作系统、同一编译器环境写构建C++项目，可以复用这个dll文件。然而当你使用其他语言时，如果这个语言读不懂dll的二进制，不知道如何与之沟通，这个语言就不能使用这个dll文件。
>
> 或者另一种情况，当你更新了这个dll文件，而应用还在用老办法调用dll，很有可能也会出错

为了解决上述问题，微软提出了**组件对象模型**（Component Object Model，COM），一套软件组件的二进制接口，可以实现跨编程语言的进程间通信、创建动态对象，在二进制层面打破了代码依赖

#### COM的优点

- 软件（apps）使用抽象接口访问服务器（servers，这里指dll文件），可以使用接口指针调用COM类的成员函数
- 软件无需知道COM的内部实现，COM对象的创建与释放由COM自行完成
- COM可能同时被多个软件使用，使用引用计数法进行GC
- 每个COM类都有独一无二的ID，因此内存中可以同时加载多个拥有相同接口的COM类，软件可以自行选择使用哪一个COM类
- COM规定了一种特殊的layout，可以被任何支持COM的语言所解析（但可惜的是，支持COM的语言并不多，因此你还是只能用C++去写DX）
- COM实际上是由指针和函数表组成（就像C++的虚函数）

#### COM的实现

COM中所有接口都继承于`IUnknown`，该接口提供了三个操作

- `AddRef`：增加引用计数的次数，每次拷贝接口指针时都会执行
- `Release`：减少引用计数的次数，当次数为0，释放对象
- `QueryInterface`：返回指向该对象的指针

不过显式控制COM对象的引用过于困难，C++推荐使用智能指针

### DXGI

DirectX Graphics Infrastructure (DXGI)，负责管理一些low-level的任务，比如如何将frame呈现在显示器上，gamma矫正，屏幕刷新，交换链等

<img src="Image/DXGI.png" alt="DXGI" style="zoom:67%;" />

### 依赖

VS添加DX12依赖

```
打开VS--项目--属性--配置属性--链接器--输入--附加依赖项
```

![image-20230112010632277](Image/添加DX依赖.png)

cmake添加依赖

```cmake
cmake_minimum_required(VERSION 3.20)
project(DXEngine)
set(CMAKE_CXX_STANDARD 17)

file(GLOB_RECURSE srcs CONFIGURE_DEPENDS src/*.cpp src/*.h)

add_executable(DXEngine WIN32 ${srcs})
target_include_directories(DXEngine PUBLIC include)

target_link_libraries(DXEngine PRIVATE
        d3d12.lib dxgi.lib dxguid.lib uuid.lib
        kernel32.lib user32.lib
        comdlg32.lib advapi32.lib shell32.lib
        ole32.lib oleaut32.lib
        runtimeobject.lib
        )
```



### 批注

VS提供了一套批注系统，SAL（Source code annotation language）

### d3dx12.h

这是一个`.h`文件，内含许多DX开发常用函数，将该文件复制到项目中

这个文件中使用了大量Windows SDK，因此你最好用VS2019的Toolchains（Clion的用户使用内置的MinGW可能会报一堆错）

至于为什么要求是VS2019，是因为这个文件与Windows10 SDK版本强相关，VS2019的SDK直接就是对应版本，2017需要手动下载，2015直接没法用

[详情](https://stackoverflow.com/questions/65294611/d3dx12-h-gives-a-bunch-of-errors)

### 创建第一个窗体

这个窗体啥也没有，就输出一个蓝色屏幕，下面是创建这个窗体的过程

![DX创建窗口](Image/DX创建窗口.png)

WindowProc是一个回调函数，用于处理传给窗口的消息

`OnInt()`是`D3D12HelloWindow`的生命周期函数，包含两个部分，加载管线和加载资源

![OnInit](Image/OnInit.png)



## 参考

[龙书代码](https://github.com/d3dcoder/d3d12book)

[learning-DX12](https://www.3dgep.com/learning-directx-12-1/)

[LearningDirectX](https://paminerva.github.io/docs/LearnDirectX/LearnDirectX)

[code](https://github.com/microsoft/DirectX-Graphics-Samples/tree/master/Samples/Desktop)