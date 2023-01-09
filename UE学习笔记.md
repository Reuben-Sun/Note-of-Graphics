# UE学习笔记

## 基类

### UObject

一切对象的基类。UE为UObject类提供了

- 垃圾回收GC
  - 被`UProperty`标记的变量会自动进行生命周期管理
  - 非UObject可以使用C++标准推荐的智能指针
- 引用自动更新
- 反射
  - 分为静态反射和动态反射，C++没有该机制（尽管C++可以在编译时进行类型推导，但远不如Java那种**Class对象**的机制好用），于是UE自己做了一套
  - 运行时知道类、函数的所有相关信息（属性表，函数表），进而实现可视化编程（蓝图，面板）
  - 通过函数名/类名+连续数据块访问对应函数/类
- 序列化
  - 资源的存储与加载
- 自动检测默认变量的更改
- 自动变量初始化
- 与Editor的交互
- 运行时类型识别
  - UE禁用了C++的`dynamic_cast`，你可以使用`Cast<>`替代
- 网络复制

### Actor

一切实体的基类。能够被挂载组件（U）

### Pawn

英语意思为棋子，指可以被操控的兵卒（可以被玩家操控，也可以被AI操控）

#### Charactor

继承自Pawn，是一个更复杂的可操控角色，该角色的特点是有一种特殊的组件，Charactor Movement

### Controller

控制器，负责控制Pawn、Charactor的行为

## 命名原则

通过类的前缀来区分类的类型

| 前缀 | 意义                           |
| ---- | ------------------------------ |
| F    | 纯C++类                        |
| U    | 继承自UObject，但不继承自Actor |
| A    | 继承自Actor                    |
| S    | Slate控件                      |
| H    | HitResult相关类                |

## 对象

### 创建对象

- F类，使用new
- U类，使用NewObject
- A类，使用SpawnActor

```c++
new FClass();
NewObject<UxxxClass>();
GetWorld()->SpawnActor<AxxxClass>();
```

## 蓝图

- UPROPERTY：注册成员变量到蓝图
- UFUNCTION：注册函数到蓝图

## 引擎基础功能

### 正则表达式

```c++
#include "Regex.h"
...
FString TextStr("This is a string");
FRegexPattern TestPattern(TEXT("C.+H"));
FRegexMatcher TestMatcher(TestPattern, TextStr);
if(TestMatcher.FindNext()){
  UE_LOG(MyLog, Warning, TEXT("找到匹配内容 %d -%d"), 
        TestMatcher.GetMatchBeginning(),
        TestMatcher.GetMatchEnding());
}
```

### 路径

```c++
//获取xxx目录路径
FString FPaths::xxxDir();		
//判断文件是否存在
bool FPaths::FileExists(const FString& InPath);	
//相对路径转化为绝对路径
FString ConvertRelativePathToFull(const FString& BasePath, FString&& InPath)；	
```

### XML

```xml
<?xml version="1.0" encoding="utf-8" ?>
<note name="Ami" age="100">
  <from>John</from>
  <list>
  	<line>Hello</line>
    <line>world</line>
  </list>
</note>
```

使用`FXmlFile`或者`FastXML`操作xml文件

```c++
FString xmlFilePath = TEXT("xxx/Test.xml");
FXmlFile* xml = new FXmlFile();
xml->LoadFile(xmlFilePath);
FXmlNode* RootNode = xml->GetRootNode();
FString from_content = RootNode->FindChildNode("from")->GetContent();
FString note_name  = RootNode->GetAttribute("name");
TArray<FXmlNode*> list_node = RootNode->FindChildNode("list")->GetChildrenNodes();
```

### JSON

```c++
FString JsonStr = "[{\"author\": \"Tim\"}, {\"age\": \"100\"}]";
TArray<TSharedPtr<FJsonValue>> JsonParsed;
TSharedRef<TJsonReader<TCHAR>> JsonReader = TJsonReaderFactory<TCHAR>::Create(JsonStr);
bool BFlag = FJsonSerializer::Deserialize(JsonReader, JsonParsed);
{
  FString FStringAutor = JsonParsed[0]->AsObject()->GetStringField("autor");
}
```

### 文件

```c++
FPlatformFileManager::Get()->GetPlatformFile();
```

### GConfig

```c+
//写配置
GConfig->SetString(TEXT("Section"), TEXT("Key"), TEXT("Value"), FPaths::xxxDir()/"Config.ini");
//读配置
FString Result;
GConfig->GetString(TEXT("Section"), TEXT("Key"), Result, FPaths::xxxDir()/"Config.ini");
```

### UE_LOG

```c++
UE_LOG(log分类，log类型，log内容)；
```

### 字符串

|         | 能否修改 | 大小写敏感 | 语意                           |
| ------- | -------- | ---------- | ------------------------------ |
| FName   | 无法修改 | 不敏感     | 名字，在整个字符串表只出现一次 |
| FText   | 无法修改 | 敏感       | 被显示的字符串                 |
| FString | 能够修改 | 敏感       | 普通字符串                     |

### 图片

`ImagerWrapper`

