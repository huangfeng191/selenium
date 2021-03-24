from main.page import PageFactory


if __name__=="__main__":
    # table=PageFactory().getTable("行业","selenium")
    table=PageFactory().getTable("行业详情","selenium")
    df=table.start()
    # table.save()
    pass
