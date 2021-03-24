class Test():
    a="12"

    def __getitem__(self,y):
        pass


if __name__ =="__main__":
    test=Test()
    a=[1,2,3]
    b=a[1]
    d=test["a"]
