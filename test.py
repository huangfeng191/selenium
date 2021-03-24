from main.page.util import ParseCommObj
if __name__=="__main__":
    obj={
        "a":1,
        "b":3,
        "c":{
            "_tp":"today_str"
        },
        "d":{
          "e":{
              "_tp":"today_str"
          }
        }
    }
    O=ParseCommObj(obj).parse()
    pass
