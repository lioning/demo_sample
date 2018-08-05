##### 简单的聊天室，client.py和server.py组成。

1. 基于asyncore/asynchat。
2. 通信协议采用"指令+参数"的格式，登录不校验。
3. 用 wxPython 来实现图形界面，
4. 用 telnetlib 来连接服务器，

##### asyncio_chat_server.py

采用异步事件库asyncio替代asyncore/asynchat，只需要提供AbstractAsyncioBase和AsyncioChat类以替代asyncore.dispatcher和asynchat.async_chat类，同时修改ChatSession和ChatServer类的初始化函数即可。



##### 收数据

 可读数据时， collect_incoming_data() -> self.data.append()

发现结束符时，found_terminator() -> command::handle(self.data)

##### 写数据

async_chat.push()