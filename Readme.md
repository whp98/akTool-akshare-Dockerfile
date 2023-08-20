# Dockerfile For Aktool Api
docker文件 用于aktool

## 运行方式 1

```shell
docker pull whp98/aktools-api:v0.0.1
```
```shell
docker run --restart=always -d -p 38080:38080 whp98/aktools-api:v0.0.1 
```


## 运行方式 2

下载源代码
进入源代码目录执行命令
```shell
docker build -t myimage .
docker run -p 38080:38080 myimage
```

## 特性
- 1.使用nginx做前置缓存
  - 默认缓存时间是1天
  - 接口可以使用 .cache_m 使用1分钟的缓存
- 2.使用Flask框架编写的web服务
- 3.默认端口是38080,请自行更改