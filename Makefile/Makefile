CC      = gcc
CXX     = g++
LINK    = g++
CFLAGS  = -g -Wall -O2
TARGET  = YOUR-TARGET
SRCS    = $(wildcard *.cpp)
SRCS    += $(wildcard *.c)
LD_PATH += /usr/local/lib
LD_LIBS += uv
INC_PATH+=

CXX_OBJS= $(patsubst %.cpp, %.o, $(wildcard *.cpp))
C_OBJS  = $(patsubst %.c, %.o, $(wildcard *.c))

all:$(TARGET)

$(TARGET):$(CXX_OBJS) $(C_OBJS)
	$(CC) $(CFLAGS) -L$(LD_PATH) $^ -l$(LD_LIBS) -o $@  
%.o:%.cpp
	$(CC) -I$(INC_PATH) $(CFLAGS) -c -o $@  $^
%.o:%.c
	$(CC) -I$(INC_PATH) $(CFLAGS) -c -o $@  $^
.PHONY:clean
clean:
	rm -rf *.o $(TARGET) $(CXX_OBJS) $(C_OBJS)