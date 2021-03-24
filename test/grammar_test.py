
class Test:
    flag=0
    def __init__(self):
        pass
        # self.flag=6
    def __new__(cls, *args, **kwargs):
        cls.flag=5
        return super(Test, cls).__new__(cls, *args, **kwargs)

    def get_flag(self):
        return self.flag

class SubTest(Test):
    flag=6
    pass
    def get_super_flag(self):
        return super().get_flag()

    def get_flag(self):
        return self.flag


def cs_init():
    print("i'm inited")

# 加载内存的时候已经执行了
class cs_init_class():
    init=cs_init()
    def get_init(self):
        print (self.init )

if __name__ =="__main__":
    pass

if __name__ =="__main__1":
    test=Test()
    print (test.get_flag())

    sub_test = SubTest()
    print(sub_test .get_flag())
    print(sub_test.get_super_flag())
